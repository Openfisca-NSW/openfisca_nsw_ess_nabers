# OpenFisca ESS NABERS

These are the rules for NABERS method of the NSW Energy Savings Scheme. 

It's based on the openfisca extension template. This repo contains the rules, tests, and constants. The parameters are defined in other repos.


## Installing

> We recommend that you [use a virtualenv](https://github.com/openfisca/country-template/blob/master/README.md#setting-up-a-virtual-environment-with-pew) to install OpenFisca. If you don't, you may need to add `--user` at the end of all commands starting by `pip`.

```sh
cd openfisca_nsw_ess_nabers
python -m venv ess 
deactivate
source ess/bin/activate
make extension

```
To install your extension, run:

```sh
python -m pip install --editable .
```

## Testing

You can make sure that everything is working by running the provided tests:

```sh
make test
```

> [Learn more about tests](http://openfisca.org/doc/coding-the-legislation/writing_yaml_tests.html).

Your extension package is now installed and ready!
