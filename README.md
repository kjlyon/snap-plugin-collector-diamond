[![Join the chat on Slack](https://intelsdi-x.herokuapp.com/badge.svg)](https://intelsdi-x.herokuapp.com/)

# A Snap collector that wraps existing Diamond collectors

[Diamond](https://github.com/python-diamond/Diamond) is a Python daemon that
collects metrics.  This snap plugin wraps Diamond plugins so they can be easily
consumed by [Snap](http://github.com/intelsdi-x/snap).

1. [Getting started](#getting-started)
 * [System requirements](#system-requirements)
 * [Installation](#installation)
 * [Example](#example)
2. [Roadmap](#roadmap)
3. [Community support](#community-support)
4. [Contributing](#contributing)
5. [License](#license)
6. [Acknowledgements](#acknowledgements)

## Getting started

### System requirements

* Python2 (>=2.7) or Python3
* Linux
* For building a package of the plugin (REWORD) 
  * [acbuild](https://github.com/containers/build) required for create a package (REWORD)
  * virtualenv or pyenv (see: [virtualenv primer](https://realpython.com/blog/python/python-virtual-environments-a-primer/))

### Installation

#### Download

You can get the pre-built plugin package for Linux (x86-64) [here](http://snap.ci.snap-telemetry.io/plugins/snap-plugin-collector-diamond/latest/linux/x86_64/snap-plugin-collector-diamond.aci).

#### To package the plugin

You will need to be on Linux with Python 2.7 or Python3 and a virtualenv activated.

I use and recommend using [pyenv](https://github.com/yyuu/pyenv) to manage my
Python version and environments.  Checkout
[pyenv-installer](https://github.com/yyuu/pyenv-installer) for an
easy installation that includes pyenv-virtualenv.  The directions below assume
that you have installed pyenv with pyenv-virtualenv.

Run the following commands from the root of the repository.

Download Python:
`pyenv install 2.7.12`

Create a virtualenv:
`pyenv virtualenv --always-copy 2.7.12 diamond27`

Activate the virtualenv:
`pyenv local diamond27`

Make the virtualenv relocatable:
`pip install virtualenv`
`virtualenv --relocatable $VIRTUAL_ENV`

Install the Python deps:
`pip install -r requirements.txt`

Create the plugin package:
`scripts/pkg.sh`

### Example

#### Start snapteld

Before the plugin can be loaded a global config entry for 'diamond' under
collectors needs to be present with entries for 'collectors_path' and
'config'.  Below is an example (diamond.yml) config:

```
---
    control:
    plugins:
        collector:
        diamond:
            versions:
            1:
                collectors_path: "/etc/diamond/collectors"
                config: |
                    {"collectors":{
                            "PingCollector": {"target_google": "8.8.8.8",
                                            "target_grafana": "grafana.net",
                                            "bin": "/bin/ping"},
                            "CPUCollector": {},
                            "DiskUsageCollector": {},
                            "MemoryCollector": {},
                            "IPCollector": {},
                            "VMStatCollector": {}
                    }}
```

To start snapteld with the above config use this command:
```snapteld -t 0 -l 1 --config diamond.yml```

#### Load the plugin

You can download the plugin package [here](http://snap.ci.snap-telemetry.io/\
plugins/snap-plugin-collector-diamond/latest/linux/x86_64/snap-plugin\
-collector-diamond.aci).  You can find more information on snap plugin
packaging [here](https://github.com/intelsdi-x/snap/blob/master/docs/\
PLUGIN_PACKAGING.md) and [here](https://intelsdi-x.github.io/snap-plugin-lib-\
py/plugin_authoring/packaging.html).

`snaptel plugin load snap-plugin-collector-diamond.aci`

An alternative approach would be to load the snap_diamond.py file however this
would require that the Python environment available to the user running
`snapteld` has all dependencies installed to it.

#### Start a task

After starting snapteld and loading the plugin we will load the following task.

```
---
  version: 1
  schedule:
    type: "simple"
    interval: "1s"
  workflow:
    collect:
      metrics:
        /diamond/*: {}
```

`snaptel task create -t examples/tasks/all.yml`

![task](https://www.dropbox.com/s/cdz5ey8skop5adf/load-create-start-task.gif?raw=1)

### Roadmap

There isn't a current roadmap for this plugin. However, if additional output types are wanted, please open an issue or submit a pull request as mentioned below. 

If you have a feature request, please add it as an [issue](https://github.com/intelsdi-x/snap-plugin-collector-diamond/issues/new) and/or submit a [pull request](https://github.com/intelsdi-x/snap-plugin-collector-diamond/pulls).

## Community Support
This repository is one of **many** plugins in **Snap**, a powerful telemetry framework. See the full project at http://github.com/intelsdi-x/snap To reach out to other users, head to the [main framework](https://github.com/intelsdi-x/snap#community-support).

[Join our Slack channel](https://intelsdi-x.herokuapp.com/).

## Contributing
We love contributions!

There's more than one way to give back, from examples to blogs to code updates. See our recommended process in [CONTRIBUTING.md](CONTRIBUTING.md).

Our code of conduct can be found [here](https://github.com/intelsdi-x/snap/blob/master/CODE_OF_CONDUCT.md).

## License
[Snap](http://github.com/intelsdi-x/snap), along with this plugin, is an Open Source software released under the Apache 2.0 [License](LICENSE).

## Acknowledgements
Original code from the [Snap](http://github.com/intelsdi-x/snap) repo.

Additional code written by:
* Author: [Joel Cooklin](https://github.com/jcooklin)

And **thank you!** Your contribution, through code and participation, is incredibly important to us.
