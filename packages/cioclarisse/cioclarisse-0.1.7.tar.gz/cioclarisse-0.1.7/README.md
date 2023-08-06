# Conductor for Clarisse

Clarisse Scripted Class submitter for the Conductor Cloud rendering service.

## Install


**To install the latest version.**
```bash
pip install --upgrade cioclarisse --target=$HOME/Conductor
```

**To install a specific version, for example 0.1.0.**
```bash
pip install --upgrade --force-reinstall cioclarisse==0.1.0 --target=$HOME/Conductor
```
**Then tell Clarisse how to find the plugin on startup.** 

Set the following path in the Startup Script section of the preferences window.

```bash
$CIO_DIR/cioclarisse/startup.py
```


## Usage

Right mouse click on a browser window and choose New->ConductorJob.

For detailed help, checkout the [tutorial](https://docs.conductortech.com/tutorials/clarisse) and [reference](https://docs.conductortech.com/reference/clarisse) documentation.

## Contributing

For help setting up your dev environment please visit [https://docs.conductortech.com/dev/contributing](https://docs.conductortech.com/dev/contributing)

Pull requests are welcome. For major changes, please [open an issue](https://github.com/AtomicConductor/conductor-clarisse/issues) to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit)