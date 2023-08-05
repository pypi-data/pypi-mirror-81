
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Byok Deployer](#byok-deployer)
- [Features](#features)
- [Prerequisites](#prerequisites)
  - [For Release](#for-release)
  - [For Development](#for-development)
- [Design](#design)
  - [Overview](#overview)
  - [Program's Define](#programs-define)
  - [Shared Lib](#shared-lib)
  - [Infra Operation](#infra-operation)
  - [Suite Related (install, uninstall, update ...)](#suite-related-install-uninstall-update)
  - [State Sync & Deployment Id](#state-sync-deployment-id)
    - [State](#state)
    - [Deployment Id](#deployment-id)
  - [Source Code Structure](#source-code-structure)
- [Development Tutorial](#development-tutorial)
  - [Use PyCharm](#use-pycharm)
    - [Prepare Env](#prepare-env)
      - [For Linux desktop](#for-linux-desktop)
      - [For Windows 10 desktop (not tested)](#for-windows-10-desktop-not-tested)
    - [Run PyCharm](#run-pycharm)
    - [Use Terminal In PyCharm](#use-terminal-in-pycharm)
  - [Create Your Suite Program](#create-your-suite-program)
    - [New Folder Structure](#new-folder-structure)
    - [Add Backend Config(mandatory)](#add-backend-configmandatory)
    - [Add Requirements(optional)](#add-requirementsoptional)
    - [Add Main Program(mandatory)](#add-main-programmandatory)
    - [Try It!](#try-it)
      - [Build](#build)
      - [Quick Run](#quick-run)
        - [Check Your Program](#check-your-program)
        - [Try Provision Infra](#try-provision-infra)
        - [Try Destroy Infra](#try-destroy-infra)
    - [Add Installation](#add-installation)
      - [Add Scripts (To Run Remotely In Bastion)](#add-scripts-to-run-remotely-in-bastion)
      - [Add Install Command](#add-install-command)
      - [Run Installation!](#run-installation)
    - [Distribute](#distribute)
- [Advanced](#advanced)
  - [Coding](#coding)
    - [Add Test](#add-test)
    - [Run Test](#run-test)
    - [Format All Code](#format-all-code)
    - [Lint Python](#lint-python)
  - [Build](#build-1)
    - [Basic usage](#basic-usage)
    - [Example](#example)
      - [Build a single program for a suite and a platform](#build-a-single-program-for-a-suite-and-a-platform)
      - [Build a suite for all platforms](#build-a-suite-for-all-platforms)
      - [Build for one platform but multiple suites](#build-for-one-platform-but-multiple-suites)
  - [CI (Jenkins Integration)](#ci-jenkins-integration)

<!-- /code_chunk_output -->

# Byok Deployer

> A common byok(bring your own k8s) deployment "framework" (I don't like this word) for create infra and install itom suites on clouds. Mainly for AWS, GCP, AZURE and even VSphere

# Features

* Support multiple python programs, easy to extend and build
* Plugable. Each program can insert/remove sub command easily
* Centerless. Can run operations across different machines
* Isolated environment. Develop in docker, Test in docker and Distribute as docker
* Flexible build. Can build and distribute one project or multiple projects at once
* Support python's standard *.tar.gz package apart from docker image
* Developer friendly. Easy to setup IDE, run test, format and lint your code.
* CI/CD friendly. Jenkins pipeline can run in docker environment same as development.
* Standard build tool for python


# Prerequisites

## For Release
* docker: ">= 17.06"

## For Development
* docker: ">= 17.06"
* docker-compose: ">= 1.26"
* gnu make

# Design

## Overview
![image](https://github.houston.softwaregrp.net/itom-deployment-automation/byok/blob/master/pics/overview.png)

This project contains mutliple python programs. Every python program will be built and named in format:

`<suite name>-<platform>`

for example,
* `<smax-gcp>`
* `<smax-azure>`

Every suite's python program here is a CLI, whose functionalities done by one or more sub commands to create/destroy infra, install/uninstall suite and others etc.

```bash
<suite>-<platform>
   --> provision
   --> destroy
   --> install
   --> uninstall
   -->
   ...
```
For example,
`smax-azure provision ..` will create infra in AZure
`smax-azure destroy ..` will destroy infra from AZure
`smax-azure install ..` will install CDF&SMAX in Azure

## Program's Define
A python package named `<suite>.<platform>` having `main.py` makes a program. For example, if a suite folder is like:

```bash
+-- smax
|   +-- gcp
|   |   +-- main.py  # entry point of the program, must have "main()"
|   +-- aws
|   |   +-- main.py  # entry point of the program, must have "main()"
```

Then here we have two programs: smax-gcp and smax-aws, which to deploy smax on gcp and aws separately.

## Shared Lib
The folder `sharelib` has common components that to be reused by suite program developers, including

* Infra operations: Provision, Destroy and Inspect etc.
* Platform base compoents: GCP, AZure and others etc.
* Utilities: Log, Download and Upload etc.


## Infra Operation
Basic infra is managed by [Terraform](https://www.terraform.io/) internally.

For example when user execute `smax-azure provision...` the program will be automatically finding terraform configures, call terraform to apply them from python (by package [pieterraform](https://pypi.org/project/pieterraform/))

Infra management is handled in sharelib so usually you **do not need** to write code for it.

## Suite Related (install, uninstall, update ...)
This is done by running scripts on remote machine (usually is bastion vm that can access database, k8s and file store in Cloud).

For example when user execute `smax-azure install...` the program will be automatically uploading CDF and SMAX packages to remote bastion and then run it using python remote package [fabric](http://www.fabfile.org/)

This is **what you need to code** for different suite because each suite may have different config and customized installation steps.

## State Sync & Deployment Id

### State
Infra operation has **STATE** saved in **Artifactory**! This is to help:
* Avoid re-create resource in Cloud
* Continue operation from last breakpoint from any machine
* Multiple people can share state so one can continue others' work easily

### Deployment Id

The **Deployment Id** works as **Unique Index** to get **Infra State** from **Artifactory**. It is passed by argument for every command.

![image](https://github.houston.softwaregrp.net/itom-deployment-automation/byok/blob/master/pics/deployment_id.png)


By a unique deployment id, any one from any machine can run any command sharing same infra!

This makes one can create infra, and then the other one can install suite based on that infra by just using same depoyment id. Finally another one can destroy infra by use that id. 

No complex config file. No many infra parameters. 
**All just an ID**! Then you get all infra information silently - the framework handle it for you!


Every command of a program by default has a parameter:

```
-x <deployment id>
```
You **Must** pass it as a **Short Unique String** while running any command. For multiple commands to share infra state, keep passing **SAME DEPLOYMENT_ID** argument for operations like provision, install, uninstall and destroy etc.

For example,

```
smax-gcp -x jevyzhu provision ....   # Create infra on GCP. Use "jevyzhu" as index of state in artifactory repo to sync infra state

smax-gcp -x jevyzhu install ....     # Install smax on GCP. Before install, get infra from artifactory by index "jevyzhu" 

smax-gcp -x jevyzhu destroy ....     # Destroy infra on GCP. Infra's state is fetched from artifactory by index "jevyzhu" 

```

Passing DEPLOYMENT_ID for each operation is a bit boring, instead you can set environment:
```
export DEPLOYMENT_ID=<my id>
```
Then all your commands in current environment will use it if you don't provide `-x` in command.



## Source Code Structure
```bash
.
+-- setup.py         # build tool
+-- Dockerfile       # build docker image to end user
+-- Dockerfile-dev   # build docker image for development (vscode remote)
+-- Makefile         # entry-points for test, build and other commands
+-- tfconfig         # all infra configs for clouds (terraform)
|   +-- gcp
|   +-- aws
|   +-- azure
|   +-- ...
|   +-- ...
+-- sharelib         # shared modules used by suites' programs
+-- <suite>          # suite projects folder, e.g. smax
|   +-- gcp
|   |   +-- main.py  # entry point of the program, must have "main()"
|   |   |   +-- install-script  # folder having script to be uploaded to remote bastion
|   +-- aws
|   |   +-- main.py
|   |   |   +-- install-script
|   +-- azure
|   |   +-- main.py
|   +-- ...
|   +-- ...

```



# Development Tutorial

## Use PyCharm

### Prepare Env

#### For Linux desktop
* Have docker and docker-compose installed
* Run command to allow x11 accept connection
```bash
xhost +
```
Note: If you don't have xhost command, please install xorg-xhost or x11-xserver-utils using your linux pacakge manager.

#### For Windows 10 desktop (not tested)
* Install [docker desktop](https://www.docker.com/products/docker-desktop)
* Install [vcxsrv](https://sourceforge.net/projects/vcxsrv/) and config it using default options
* Set env `DISPLAY` to `<your ip>:0.0`

### Run PyCharm

Clone this repo and then run:

```bash
make docker-dev

docker exec byok-devenv make setup-pycharm   # install pycharm and set it 

docker exec byok-devenv make start-pycharm   # start pycharm in docker
```

This **PyCharm** will be **Running In Docker** !

Note: `make setup-pycharm` **only need to be run at the first time**.

Next time, just run

```bash
docker exec byok-devenv make start-pycharm
```
to boot up PyCharm from docker.

### Use Terminal In PyCharm
Just open terminal panel in PyCharm immediately you have bash in container `byok-devenv`.

## Create Your Suite Program
Assuming you want to addd a program for suite named "**WuKong**" on "**GCP**"
Please follow steps below.

### New Folder Structure
Open terminal in PyCharm then run:
```bash
mkdir -p WuKong/gcp
touch WuKong/__init.py__
touch WuKong/gcp/__init.py__
```
### Add Backend Config(mandatory)
Add a new file named `backend.config` under WuKong/gcp with content like:
```toml
url = "https://shcartifactory.swinfra.net/artifactory"
repo = "itom-generic-sma-local"
```
Just put in our artifactory URL and the repo name (must exists). Our program will use artifactory to save status.

### Add Requirements(optional)
Say, WuKong wants to use 3rd-party python packages like request.
Add a new file named `requirements.txt` under WuKong/gcp with content like:
```toml
requests~= 2.24.0
```

### Add Main Program(mandatory)
Add a new file named `main.py` under WuKong/gcp with content like:
```python

from sharelib.gcp.gcp_program import GcpProgram

class MyProgram(GcpProgram):
    @property
    def version(self) -> str:
        return "1.0.0"             # Your program's version

    @property
    def program_name(self) -> str:
        return "wukong-gcp"        # Your program's name

    def add_subcommands(self):
        super().add_subcommands()

    @property
    def module(self) -> str:
        return __file__


def main():                        # MUST HAVE!!
    MyProgram().run()

if __name__ == "__main__":
    main()

```

### Try It!
#### Build
Open terminal in PyCharm then run:
```bash
export BUILD_SUITE=WuKong
export BUILD_PLATFORM=gcp
make
```
#### Quick Run

##### Check Your Program

Open terminal in PyCharm then run:

```bash
python -m WuKong.gcp.main --help
python -m WuKong.gcp.main --version
```

You will see **big output** like:
```
$ python -m WuKong.gcp.main --help
----------------------------------

usage: main.py [-h] [--version] [-x DEPLOYMENT_ID] -atu ARTIFACT_USER -atp
               ARTIFACT_PASSWORD [--color-log] [--no-cache] [--debug]
               [-t TF_CONFIG_NAME]
               {provision,destroy,tfshow} ...

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -x DEPLOYMENT_ID, --deployment-id DEPLOYMENT_ID
                        id to mark provision, install and destroyby default
                        use env: DEPLOYMENT_ID (default: testonly)
  -atu ARTIFACT_USER, --artifact-user ARTIFACT_USER
                        terraform backend(artifactory) userby default use env:
                        ARTIFACT_USER (default: )
  -atp ARTIFACT_PASSWORD, --artifact-password ARTIFACT_PASSWORD
                        terraform backend(artifactory) passwordby default use
                        env: ARTIFACT_PWD (default: )
  --color-log           Use color log (default: False)
  --no-cache            clean after run (default: False)
  --debug               Output log in debug level (default: False)
  -t TF_CONFIG_NAME, --tf-config-name TF_CONFIG_NAME
                        terraform config name (default: test)

commands =>:
  {provision,destroy,tfshow}
    provision           Create all infra on GCP
    destroy             Destroy all infra on GCP
    tfshow              Inspect infra

$ python -m WuKong.gcp.main  --version
---------------------------------------
wukong-gcp 1.0.0
```

**EASY!**  - just a few lines of code but you get so much!!

##### Try Provision Infra

Now you are ready to create resources on GCP!!

Open terminal in PyCharm then run:

```bash
$ python -m WuKong.gcp.main -x <DEPLOYMENT_ID> -atu <ARTIFACTORY_USER> -atp <ARTIFACTORY_PASSWORD> provision -k <GCP_SVC_KEY_FILE>
```

You must provide:
* Your artifactory user/password
* Gcp key file (from GCP)
* A deployment id

Note: **DEPLOYMENT_ID is important**. It is to make your infra unique and the program will be using it to sync your infra state from artifactory.
The benefit is if the provision interrupted while running, leaving some resoruces created in GCP. Next time running same command in same or another machine the program will continue from last breakpoint and existing resources in GCP will not be recreated!

##### Try Destroy Infra
You can destroy all in one line command.
Open terminal in PyCharm then run:
```bash
$ python -m WuKong.gcp.main -x <DEPLOYMENT_ID> -atu <ARTIFACTORY_USER> -atp <ARTIFACTORY_PASSWORD> destroy -k <GCP_SVC_KEY_FILE>
```

### Add Installation

Now let's run script on infra's bastion

#### Add Scripts (To Run Remotely In Bastion)
* Add a folder named `install-script` under WuKong/gcp
```base
mkdir -p WuKong/gcp/install-script
```
Note: By default, you **must** name the folder as `install-script` though it can be customized. 
Note: You **do not need** to care how to upload files under `install-script` folder because the framework **upload files under the folder for you automatically**!!

* Add a script e.g. named `install-wukong.sh` under WuKong/gcp/install-script, with content as:
```bash
#!/bin/bash
echo WuKong Installed ^0^
```
Here I just print something. In real work, please write script as you need.

#### Add Install Command

* Add a new file named `install.py` under WuKong/gcp with content like:
```python

import shutil
from argparse import ArgumentParser
from sharelib.base_install import BaseInstall

class WuKongInstall(BaseInstall):
    @property
    def name(self):
        return "install-wukong"

    @property
    def help(self):
        return "Install WuKong to Gcp"

    def args(self, sub_parser: ArgumentParser):
        super().args(sub_parser)
        sub_parser.add_argument(
            "--size",
            dest="size",
            default="small",
            type=str,
            required=False,
        )

    def the_act(self, args):
        super().the_act(args)
        self.run_in_bastion("./install-wukong.sh")  # run command in remote bastion
        self.logger.info("WuKong Installed!")
```

* Add WuKongInstall
Edit `main.py` by adding WuKongInstall into `add_subcommands(self)`
```python
...
...
from .install import WuKongInstall #import WuKongInstall
...

class MyProgram(GcpProgram):
...
...

  def add_subcommands(self):
      super().add_subcommands()
      self.simple_parser.add_sub_cmd(WuKongInstall()) # Add WuKongInstall

...
...

```

#### Run Installation!
Open terminal (in PyCharm) and then run:
```
# Create GCP infra

$ python -m WuKong.gcp.main -x <DEPLOYMENT_ID> -atu <ARTIFACTORY_USER> -atp <ARTIFACTORY_PASSWORD> provision -k <GCP_SVC_KEY_FILE>

# Install WuKong (run wukong-install.sh in bastion created in above command)

$ python -m WuKong.gcp.main -x <DEPLOYMENT_ID> -atu <ARTIFACTORY_USER> -atp <ARTIFACTORY_PASSWORD> install-wukong
```

**Hint**: Input artifactory user and password for every operation is boring. Instead you can set environments at once:

```bash
export ARTIFACT_USER=<user>
export ARTIFACT_PWD=<password>
```
Note: The artifactory user must **be able to write** into repo.

Then following commands will use above environments automatically.

### Distribute
Open terminal (not in PyCharm) and then run:
```
export BUILD_SUITE=WuKong
export BUILD_PLATFORM=gcp
make docker
```
This will build a image tagged `WuKong-gcp` for you. The image has `wukong-gcp` installed in it automatically.
You can run the image using docker:
```
docker run WuKong-gcp wukong-gcp
```

# Advanced

## Coding

### Add Test
Create python file named `test...` in folder tests/, just following existing sample:
`tests/test_smax_gcp.py`.

### Run Test
```
make test
```

### Format All Code
```
make fmt
```

### Lint Python
```
make lint
```

## Build

### Basic usage
```bash
export BUILD_SUITE=<suite>
export BUILD_PLATFORM=<platform>

make docker    # build docker image
make dist      # build python .tar.gz package
make install   # install to local machine
```

### Example

#### Build a single program for a suite and a platform
* This way a suite deployer distribution with one platform program in one place
```bash
export BUILD_SUITE=smax
export BUILD_PLATFORM=gcp

make docker      # docker image, has program smax-gcp
make dist        # generate a smax-gcp.<version>.tar.gz under dist/
make install     # install smax-gcp to local machine
```

#### Build a suite for all platforms
* This way a suite deployer distribution with multiple platforms programs in on place
```bash
export BUILD_SUITE=smax
export BUILD_PLATFORM=

make docker      # docker image, has programs smax-gcp, smax-aws and smax-azure ... as long as implemented
make dist        # generate multiple smax-<platform>.<version>.tar.gz under dist/
make install     # install smax-gcp, smax-aws, smax-azure ...  to local machine
```

#### Build for one platform but multiple suites
* This way a platform deployer distribution with multiple suites  programs in on place
```bash
export BUILD_SUITE=
export BUILD_PLATFORM=gcp

make docker      # docker image, has programs smax-gcp, dca-gcp and opsb-gcp ... as long as implemented
make dist        # generate multiple <suite>-gcp.<version>.tar.gz under dist/
make install     # install smax-gcp, dca-gcp, opsb-gcp ...  to local machine
```

## CI (Jenkins Integration)
To build me in jenkins is easy. Just use two dockerfiles in your pipeline:

* Dockerfile-dev: Run build, lint, and test

* Dockerfile: Generate docker image for end user

You **do not need** to setup anything for any Jenkins node. Everything is done in docker.
