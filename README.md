# plonectl

NextGen CLI controller for Plone

## Installation

Install plonectl with `pip`:

```shell
pip install plonectl
```

## Usage

### Configuration

On the root folder of your project, create a `plone.yaml` file with configuration:

```yaml
instance:
    initial_user_name: 'admin'
    initial_user_password: 'admin'

    load_zcml:
        package_includes: []

    db_storage: direct
```
All options can be seen on [default.yaml](./src/plonectl/settings/default.yaml) file.

## Develop

Clone this codebase

```shell
git clone git@github.com:plone/plonectl.git
```

Install code with development packages:

```shell
make install
```

Run tests

```shell
make test
```


## Contribute

- [Issue Tracker](https://github.com/plone/plonectl/issues)
- [Source Code](https://github.com/plone/plonectl/)

## License

The project is licensed under GPLv2.
