[![Build Status](https://github.com/adegomme/aiida-sshonly/workflows/ci/badge.svg?branch=master)](https://github.com/adegomme/aiida-sshonly/actions)
[![Coverage Status](https://coveralls.io/repos/github/adegomme/aiida-sshonly/badge.svg?branch=master)](https://coveralls.io/github/adegomme/aiida-sshonly?branch=master)
[![Docs status](https://readthedocs.org/projects/aiida-sshonly/badge)](http://aiida-sshonly.readthedocs.io/)
[![PyPI version](https://badge.fury.io/py/aiida-sshonly.svg)](https://badge.fury.io/py/aiida-sshonly)

# aiida-sshonly

AiiDA plugin adding a sshonly transport option, using only SSH to transfer files, avoiding SFTP, in case it's blocked or non functional on a remote system


## Features

Provides a new 'sshonly' transport option when configuring a computer in AiiDA.
Uses SSH and shell commands to emulate SFTP commands used in AiiDA.

Known limitation : only works with text files as of 0.1.0

## Installation

```shell
pip install aiida-sshonly
reentry scan
verdi plugin list aiida.transports  # should now show your calclulation plugins
```


## Usage

Here goes a complete example of how to submit a test calculation using this plugin.

A quick demo of how to submit a calculation:
```shell
verdi daemon start     # make sure the daemon is running
cd examples
./example_01.py        # run test calculation
verdi process list -a  # check record of calculation
```

The plugin also includes verdi commands to inspect its data types:
```shell
verdi data sshonly list
verdi data sshonly export <PK>
```

## Development

```shell
git clone https://github.com/adegomme/aiida-sshonly .
cd aiida-sshonly
pip install -e .[pre-commit,testing]  # install extra dependencies
pre-commit install  # install pre-commit hooks
pytest -v  # discover and run all tests
```

See the [developer guide](http://aiida-sshonly.readthedocs.io/en/latest/developer_guide/index.html) for more information.

## License

MIT


