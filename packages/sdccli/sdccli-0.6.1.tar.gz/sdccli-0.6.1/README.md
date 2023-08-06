# Sysdig Platform CLI - Internal documetation

The Sysdig Platform CLI (or sdc-cli) is a unified tool implemented using [Sysdig Python SDK](https://github.com/sysdiglabs/sysdig-sdk-python) to manage Sysdig Monitor and Sysdig Secure using your terminal. 

## Internal documentation

This is the internal documentation available to partners. It only contains specifics for those with access to the git repository. Additional information is available on the [public documentation website](https://sysdiglabs.github.io/sysdig-platform-cli).

## Set up

You can set up or install the _Sysdig Platform CLI_ in several ways:

* Using a docker image
  * Pulled from Dockerhub public registry
  * Building your own image (_internal_)
* Installing the binary using `pip`
  * Globally
  * In virtual environment
* Build and install from Python sources (_internal_)
* Download binary from [latest release](https://github.com/sysdiglabs/sysdig-platform-cli/releases/latest) (_internal_)

The following instructions describe the procedures for internal users. To check those publicly available, visit the [public documentation website](https://sysdiglabs.github.io/sysdig-platform-cli#).

### Download binary from latest release

Visit the [latest release](https://github.com/sysdiglabs/sysdig-platform-cli/releases/latest) webpage of this repository, 

### Building your own image

You can build and use your own docker image from the latest source. After cloning this repository, run:

```bash
docker build -t sdc-cli .
docker run -v .:/data sdc-cli [options]
```
Then you can use the image in a similar way as the one pulled from Dockerhub public repository

```bash
# Passing configuration using environment variables
$ docker run -v .:/data -e SDC_MONITOR_TOKEN=<token> -e SDC_SECURE_TOKEN=<token> sysdiglabs/sdc-cli [options]
# Using a configuration file
$ docker run -v .:/data -v /path/to/config.yaml:/etc/sdc-cli/config.yml sysdiglabs/sdc-cli [options]
```

Check the [public documentation website](https://sysdiglabs.github.io/sysdig-platform-cli#) for more information about Docker image usage.

### Manual installation from sources

Make sure Python 3 is installed

```bash
$ python3 -V
Python 3.8.5
```

It is recommended to use *virtualenv* to isolate the execution environment. See[this link to the virtualenv documentation](http://virtualenv.readthedocs.org/en/latest/) for more instructions about how to install it. 

To create a new virtual environment, after clonning this repo and from the main directory, execute:

```bash
$ virtualenv -p python3.8 venv
Already using interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in /home/vicen/code/sysdig-platform-cli/venv/bin/python3
Also creating executable in /home/vicen/code/sysdig-platform-cli/venv/bin/python
Installing setuptools, pkg_resources, pip, wheel...done.
```

Activate the new virtual environment using bash (see [virtualenv docmentation for other shells](https://virtualenv.readthedocs.io/en/latest/user_guide.html#activators)), use:

```bash
$ source venv/bin/activate
```

Execute the installation on this environment

```bash
$ python3 setup.py install
```

Now the sdc-cli binary should be available to you, and you can invoke it directly with:

```bash
$ sdc-cli
```

Remember that before starting to use it, you have to activate the virtual environment from the repository directory.

To deactivate the virtual environment, use:
```bash
$ deactivate
```


## Usage

See the [public documentation](https://sysdiglabs.github.io/sysdig-platform-cli) for usage instructions and examples.
