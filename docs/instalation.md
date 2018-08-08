# Installation

## Python Version

neo-cli only support Python 3 or newer.

## Python3

Don't worry if you don't have Python3 installed. It's save to install
Python3 alongside Python2. Both have different installation location.

You can get python3 from your distro (GNU/Linux distribution) repository.

``` bash
$ sudo apt-get install python3
```
Use `python3` instead of `python` when you want to use python3.

`which` help you tell you what program you are using (e.g `which python3`)

## pip

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

## Virtual environments

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

## Dependencies

Dependencies are located in [requirements](requirements.txt)

Grab those dependencies with

``` bash
$ pip3 install -r requirements.txt
```

## Install neo-cli

``` bash
pip3 install -e .
```
Test if NEO installed correctly

``` bash
neo --help
```
If you get the help output from neo. Then you are ready to have fun.

## Troubleshooting

### `Unable to locate package python3-venv`

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


### `No command 'neo' found`

Make sure you virtual environments is activated
