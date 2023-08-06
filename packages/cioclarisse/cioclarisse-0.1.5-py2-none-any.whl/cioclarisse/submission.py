"""
Build an object to represent a Clarisse Conductor submission.

In this case the submission may contain xrefs nested to any level and we do a
pretty good job of resolving them. However, if the render errors due to xref
the localize method is the fallback.
"""

import errno

import os
import re
import shutil
import sys
import tempfile
import traceback

import cioclarisse.clarisse_config as ccfg
import cioclarisse.dependencies as deps
import cioclarisse.utils as cu
import ix

from cioclarisse.job import Job
from ciocore import conductor_submit
from cioclarisse.utils import ConductorError
from ciocore import data as coredata

from ciocore.gpath import Path
 

FILE_ATTR_HINTS = [
    ix.api.OfAttr.VISUAL_HINT_FILENAME_SAVE,
    ix.api.OfAttr.VISUAL_HINT_FILENAME_OPEN,
    ix.api.OfAttr.VISUAL_HINT_FOLDER,
]


def _get_path_line_regex():
    """
    Generate a regex to help identify filepath attributes.

    As we scan project files to replace windows paths, we use this regex which
    will be something like: r'\s+(?:filename|filename_sys|save_as)\s+"(.*)"\s+' 
    only longer.
    """
    classes = ix.application.get_factory().get_classes()
    file_attrs = []
    for klass in classes.get_classes():
        attr_count = klass.get_attribute_count()
        for i in xrange(attr_count):
            attr = klass.get_attribute(i)
            hint = attr.get_visual_hint()
            if hint in FILE_ATTR_HINTS:
                file_attrs.append(attr.get_name())

    return r"\s+(?:" + "|".join(sorted(set(file_attrs))) + r')\s+"(.*)"\s+'


def _remove_conductor():
    """
    Remove all Conductor data from the render archive.

    This ensures the render logs are not polluted by complaints about Conductor
    nodes. This can only be done in the situation where we localize contexts,
    because in that case we get to reload the scene after submission.
    """
    objects = ix.api.OfObjectArray()
    ix.application.get_factory().get_objects("ConductorJob", objects)
    for item in list(objects):
        ix.application.get_factory().remove_item(item.get_full_name())


class Submission(object):
    """
    Submission holds all data needed for a submission.

    It has potentially many Jobs, and those Jobs each have many Tasks. A
    Submission can provide the correct args to send to Conductor, or it can be
    used to create a dry run to show the user what will happen.

    A Submission also sets a list of tokens that the user can access as <angle
    bracket> tokens in order to build strings in the UI such as commands, job
    title, and (soon to be added) metadata.
    """

    def __init__(self, obj):
        """
        Collect data from the Clarisse UI.

        Collect attribute values that are common to all jobs, then call
        _set_tokens(). After _set_tokens has been called, the Submission level
        token variables are valid and calls to evaluate expressions will
        correctly resolve where those tokens have been used.
        """
        self.node = obj

        if self.node.is_kindof("ConductorJob"):
            self.nodes = [obj]
        else:
            raise NotImplementedError

        self.project_filename = ix.application.get_current_project_filename()
 
        self.tmpdir = Path(
            os.path.join(
                ix.application.get_factory().get_vars().get("CTEMP").get_string(),
                "conductor",
            )
        )
        self.render_package_path = self._get_render_package_path()
        self.local_upload = self.node.get_attribute("local_upload").get_bool()

        self.should_delete_render_package = (
            self.node.get_attribute("clean_up_render_package").get_bool()
            and self.local_upload
        )

        self.upload_only = self.node.get_attribute("upload_only").get_bool()
        self.project = self._get_project()
        self.notifications = self._get_notifications()
        self.tokens = self._set_tokens()

        self.jobs = []
        for node in self.nodes:
            job = Job(node, self.tokens, self.render_package_path)
            self.jobs.append(job)

    def _get_project(self):
        """Get the project from the attr.

        Get its ID in case the current project is no longer in the list
        of projects at conductor, throw an error.
        """


        projects = coredata.data().get("projects")
        project_att = self.node.get_attribute("conductor_project_name")
        label = project_att.get_applied_preset_label()

        found = next((p for p in projects if p== label), None)
        if not found:
            msg = 'Cannot find project "{}" at Conductor. Please ensure the PROJECT dropdown contains a valid project.'.format(label)
            raise ConductorError(msg)

        return found

    def _get_notifications(self):
        """Get notification prefs."""
        if not self.node.get_attribute("notify").get_bool():
            return None

        emails = self.node.get_attribute("email_addresses").get_string()
        return [email.strip() for email in emails.split(",") if email.strip()]

    def _set_tokens(self):
        """Env tokens are variables to help the user build expressions.

        The user interface has fields for strings such as job title,
        task command. The user can use these tokens with <angle brackets> to build those strings. Tokens at the Submission
        level are also available in Job level fields, and likewise
        tokens at the Job level are available in Task level fields.
        """
        tokens = {}

        pdir_val = ix.application.get_factory().get_vars().get("PDIR").get_string()

        tokens["pdir"] = '"{}"'.format(Path(pdir_val).posix_path(with_drive=False))

        tokens["temp_dir"] = "{}".format(self.tmpdir.posix_path(with_drive=False))
        tokens["submitter"] = self.node.get_name()

        tokens["render_package"] = '"{}"'.format(
            self.render_package_path.posix_path(with_drive=False)
        )

        tokens["project"] = self.project 

        return tokens

    def _get_render_package_path(self):
        """
        Calc the path to the render package.

        The name is not always known until
        preview/submission time because it is based on the filename. 

        It will however always show up in the preview window.

        We replace spaces in the filename because of a bug in Clarisse
        https://www.isotropix.com/user/bugtracker/376

        Returns:
            string: path
        """

        msg= 'Cannot create a submission from this file. Has it ever been saved?'
        current_filename = ix.application.get_current_project_filename()
        if not current_filename:
            raise ConductorError(msg)

        node_name =self.node.get_attribute("title").get_string()

        node_name = "".join(x for x in node_name if x.isalpha() or x.isdigit()  )


        path = os.path.splitext(current_filename)[0]

        path = os.path.join(
            os.path.dirname(path), os.path.basename(path).replace(" ", "_")
        )
 
        return Path("{}.{}.cio.project".format(path,node_name))

    def get_args(self):
        """
        Prepare the args for submission to conductor.

        Returns:
            list: list of dicts containing submission args per job.
        """

        result = []
        submission_args = {}

        submission_args["local_upload"] = self.local_upload
        submission_args["upload_only"] = self.upload_only
        
        submission_args["project"] = self.project
        submission_args["notify"] = self.notifications

        for job in self.jobs:
            args = job.get_args(self.upload_only)
            args.update(submission_args)
            result.append(args)
        return result

    def submit(self):
        """
        Submit all jobs.

        Returns:
            list: list of response dictionaries, containing response codes
            and descriptions.
        """

        submission_args = self.get_args()
        self._before_submit()

        self.remove_missing_upload_paths(submission_args)
        
        results = []
  
        for job_args in submission_args:
            try:
                remote_job = conductor_submit.Submit(job_args)
                response, response_code = remote_job.main()
                results.append({"code": response_code, "response": response})
            except BaseException:
                results.append(
                    {
                        "code": "undefined",
                        "response": "".join(
                            traceback.format_exception(*sys.exc_info())
                        ),
                    }
                )
        for result in results:
            ix.log_info(result)
 
        self._after_submit()
        return results

    def _before_submit(self):
        """
        Prepare the project files that will be shipped.

        We first write out the current project file. 
        
        Then (on Windows) we find additional referenced project 
        files and adjust paths in all of them so they may be 
        rendered on linux render nodes.
        """
        self.write_render_package()


    def write_render_package(self):
        """
        Write a package suitable for rendering.

        A render package is a project file with a special name.
        """

        self._before_write_package()

        context = ix.get_item("project:/")
        ix.log_info("Writing render package: context is '{}'".format(context))
            
        package_file = self.render_package_path.posix_path()

        with cu.disabled_app():
            success = ix.export_context_as_project_with_dependencies(context, package_file)
        
        if success:
            ix.log_info("Wrote render package '{}'".format(package_file))
        else:
            msg = "Failed to write render package file '{}'".format(package_file)
            raise ConductorError(msg)

        self._after_write_package()

        if cu.is_windows():
            ix.log_info("Windows path adjustments")
            self._linuxify_render_package()
            ix.log_info("Linuxified render project file")
        else:
            ix.log_info("Not using Windows")

        return package_file

    def _linuxify_render_package(self):
        """
        Adjust reference pasths for windows.
        """

        temp_path = os.path.join(
            tempfile.gettempdir(), next(tempfile._get_candidate_names())
        )
        shutil.copy2(self.render_package_path.posix_path(), temp_path)

        os.remove(self.render_package_path.posix_path())
        self._linuxify_file(
            temp_path, self.render_package_path.posix_path()
        )

    def _linuxify_file(self, filename, dest_path=None):
        """
        Fix paths for one file.

        If the file already has the .ct.project extension, replace it too.
        """
        path_regex = _get_path_line_regex()

        out_filename = dest_path

        with open(out_filename, "w+") as outfile:
            with open(filename, "r+") as infile:
                for line in infile:
                    outfile.write(self._replace_path(line, path_regex))

    def _replace_path(self, line, path_regex):
        """
        Detect paths in the line of text and make a replacement.

        Args:
            line (string): line from the file.

        Returns:
            string: The line, possibly with replaced path
        """

        match = re.match(path_regex, line)
        if match:
            path = Path(match.group(1), no_expand=True).posix_path(with_drive=False)

            return line.replace(match.group(1), path)

        return line

    def remove_missing_upload_paths(self, submission_args):
        """
        Alert the user of missing files. If the user doesn't want to continue
        with missing files, the result will be False. Otherwise it will be True
        and the potentially adjusted args are returned.

        Args:
            submission_args (list): list of job args.

        Returns:
           tuple (bool, adjusted args):
        """
        missing_files = []

        for job_args in submission_args:
            existing_files = []
            for path in job_args["upload_paths"]:
                if os.path.exists(path):
                    existing_files.append(path)
                else:
                    missing_files.append(path)

            job_args["upload_paths"] = existing_files

        missing_files = sorted(list( missing_files))
        if missing_files:
            ix.log_warning("Skipping missing files:")
            for f in missing_files:
                ix.log_warning(f)


    def _before_write_package(self):
        """
        Prepare to write render package.
        """
        self._prepare_temp_directory()
        self._copy_system_dependencies_to_temp()

    def _prepare_temp_directory(self):
        """
        Make sure the temp directory has a conductor subdirectory.
        """
        tmpdir = self.tmpdir.posix_path()
        try:
            os.makedirs(tmpdir)
        except OSError as ex:
            if not (ex.errno == errno.EEXIST and os.path.isdir(tmpdir)):
                raise
        ix.log_info("Prepared tmpdir '{}'".format(tmpdir))

    def _copy_system_dependencies_to_temp(self):
        """
        Copy over all system dependencies to a tmp folder.

        Wrapper scripts, config files etc. The clarisse.cfg file is special. See
        ../clarisse_config.py
        """
        for entry in deps.system_dependencies():
            if os.path.isfile(entry["src"]):
                if entry["src"].endswith(".cfg"):
                    safe_config = ccfg.legalize(entry["src"])
                    with open(entry["dest"], "w") as dest:
                        dest.write(safe_config)
                    ix.log_info(
                        "Copy with mods {} to {}".format(entry["src"], entry["dest"])
                    )
                else:
                    ix.log_info("Copy {} to {}".format(entry["src"], entry["dest"]))
                    shutil.copy(entry["src"], entry["dest"])


    def _after_submit(self):
        """Clean up, and potentially other post submission actions."""
        self._delete_render_package()

    def _after_write_package(self):
        """
        Runs operations after saving the render package.

        If we did something destructive, like localize contexts, then
        a backup will have been saved and we now reload it. This strategy
        is used because Clarisse's undo is broken when it comes to
        undoing context localization.
        """
        pass
 
    def _delete_render_package(self):
        """
        Delete the render package from disk if the user wants to.
        """
        if self.should_delete_render_package:
            render_package_file = self.render_package_path.posix_path()
            if os.path.exists(render_package_file):
                os.remove(render_package_file)
 

    @property
    def node_name(self):
        """node_name."""
        return self.node.get_name()

    @property
    def filename(self):
        """filename."""
        return ix.application.get_current_project_filename()

    def has_notifications(self):
        """has_notifications."""
        return bool(self.notifications)

    @property
    def email_addresses(self):
        """email_addresses."""
        if not self.has_notifications():
            return []
        return self.notifications["email"]["addresses"]
