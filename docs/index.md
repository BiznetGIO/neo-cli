# neo-cli 

Agnostic Orchestration Tools for Openstack

---

## Installation

### Python Version

neo-cli only support Python 3 or newer.

Don't worry if you don't have Python3 installed. It's save to install
Python3 alongside Python2. Both have different installation location.

You can get python3 from your distro (GNU/Linux distribution) repository.

``` bash
$ sudo apt-get install python3
```
Use `python3` instead of `python` when you want to use python3.

`which` help you tell you what program you are using (e.g `which python3`)

### pip

Get the pip for python3 with the following steps

``` bash
$ curl -O https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py
```
Then use pip with `pip3`.

Another way is to get it from your distro repository

``` bash
$ sudo apt-get install python3-pip
```

### Virtual environments

We strongly recommend using virtual environments to manage
dependencies of your project.

``` bash
$ sudo apt-get install python3-venv
```

Make new virtual environments with

``` bash
$ python3 -m venv yourvenvname
```
Active the venv (virtual environments) with

``` bash
$ source yourvenvname/bin/activate
```
Check if it's activated with

``` bash
$ which python3
```
If the output point to yourvenvname location. Then you are set.

Deactivate venv with

``` bash
$ deactivate
```

### Dependencies

Dependencies are located in requirements.txt

Grab those dependencies with

``` bash
$ pip3 install -r requirements.txt
```

### Install neo-cli

``` bash
pip3 install -e .
```
Test if NEO installed correctly

``` bash
neo --help
```
If you get the help output from neo. Then you are ready to have fun.

---

## Usage

You can list all NEO command with `help`

``` bash
$ neo --help
```

### Authentication

Use `neo login` to log in. `neo logout` to do the opposite.

### Creation

``` bash
$ neo create
```

NEO creates `neo.yml` for you if it doesn't find one. Then it will
guide you trough questions to do the right job for you.

It will ask you the 'stack' and 'template' you want to create. Then
fill 'key-pairs' and 'network' configuration. The last step is to
setup your 'vm' where you are asked to choose 'image name' and
'flavor'.

When you sure with the configuration. Hit 'y/yes' to continue to
deploy.

### List your stuffs

``` bash
$ neo ls --help
```

- `stack`

List all the stacks

- `vm`

List all virtual machines

- `network`

List all network

e.g `neo ls stack`

### Remove your stuffs

``` bash
$ neo rm
```

It will delete your stack, network and machine

### Update

``` bash
$ neo update
```
Use `update` to see your changes.

### Attach

Attach local standard input, output, and error streams to a running
stack or virtual machine


``` bash
$ neo attach vm
```

`neo attach` will read neo.yml configuration automatically if you
didn't pass the <id> of your vm.

You can also specify your running vm id manually with

``` bash
$ neo attach vm <your-vm-id>
```

---

## Troubleshooting

### Unable to locate package python3-venv

Try to check the python3 venv module name provided by your distro

``` bash
$ apt-cache search python3 | grep venv
```
The results

``` bash
python3-venv - pyvenv-3 binary for python3 (default python3 version)
python3.5-venv - Interactive high-level object-oriented language (pyvenv binary, version 3.5)
```
It might be differ on your machine. So please make sure you get the
correct name.

### No command 'neo' found

Make sure you virtual environments is activated
