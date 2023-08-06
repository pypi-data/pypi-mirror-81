# Conductor for Cinema 4d

Cinema 4d plugin submitter for the Conductor Cloud rendering service.

## Install

**To install the latest version.**
```bash
pip install --upgrade cioc4d --target=$HOME/Conductor
```

**To install a specific version, for example 0.1.0.**
```bash
pip install --upgrade --force-reinstall cioc4d==0.1.0 --target=$HOME/Conductor
```

## Usage

Go to **Edit->Preferences->Plugins** and add the path to the cioc4d installation directory. 

```
~/Conductor/cioc4d
```

restart Cinema 4d.

To set up a render, choose **Conductor->ConductorRender**. 

For detailed help, checkout the [tutorial](https://docs.conductortech.com/tutorials/c4d) and [reference](https://docs.conductortech.com/reference/c4d) documentation.

## Contributing

For help setting up your dev environment please visit [https://docs.conductortech.com/dev/contributing](https://docs.conductortech.com/dev/contributing)

Pull requests are welcome. For major changes, please [open an issue](https://github.com/AtomicConductor/conductor-maya/issues) to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit)
