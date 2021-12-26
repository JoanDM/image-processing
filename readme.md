# Image processing
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.9.5=0](https://img.shields.io/badge/python-3.9.5-blue.svg)](https://www.python.org/downloads/release/python-395/)

Set of tools used for handy image processing workflows such as:

* Labeling sequences of frames with OpenCV tracking algorithms

https://user-images.githubusercontent.com/29776287/147406522-9f564753-4757-4ff4-9448-295b02f2b238.mov

* Create physical labels to identify products in a database

https://user-images.githubusercontent.com/29776287/147406215-2f8e80b2-b18c-4b62-8b42-343996e97fb9.mov

* Extracting frames from videos 

https://user-images.githubusercontent.com/29776287/147124345-b70f87e4-4c77-4bee-82ec-ce4217bec5fb.mov

# QuickStart: One-time setup

Before anything, you must have pyenv installed in order to run the scripts smoothly.
[How to setup pyenv](#pyenv-guide-for-handling-multiple-python-versions-in-your-mac)

In case you have autoenv installed, the repo should get automatically set up as soon as you `cd image-processing`. :crystal_ball:
[How to setup autoenv](#guide-for-ultimate-repository-setup-with-autoenv)

In case you don't have autoenv, you can also manually set up the environment by running:
```bash
cd image-processing
python -mvenv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
export PYTHONPATH=$(pwd)
```
Now you should be able to run the scripts

In order to not increase the repository size too much, store big files on git LFS. Make sure you have it installed on your Mac
([How to get git LFS with Homebrew](https://formulae.brew.sh/formula/git-lfs)).

You might have to run `git lfs pull` to download the files.

If you want to contribute to the codebase, make sure you set the pre-commit hooks before committing code changes.
[How to set pre-commit hooks](#code-formatting)

# Code formatting
Code formatting is enforced with [Black](https://black.readthedocs.io/).
 
On your local repo, you can automatically run Black formatting using a pre-commit hook. 
The required configuration is in the file `.pre-commit-config.yaml`. 
You will need Python packages `black` and `pre-commit` install for this.

To install the pre-commit hook, run the following command inside your repo
```shell
$ pre-commit install
```

After having installed the pre-commit hook, a commit that is not formatted correctly will be aborted, 
and the offending code will automatically be reformatted. 
Review the formatting changes, stage them and re-run the commit.

# Pyenv guide for handling multiple python versions in your Mac

With [pyenv](https://formulae.brew.sh/formula/pyenv) you can easily switch python versions. It's specially handy when you work with multiple python-based repositories with particular dependencies and virtual environments.

Through pyenv, the current repository defines the Python version to be used in `.python-version`.

First, install pyenv through Homebrew
```shell
$ brew update
$ brew install pyenv
```

Then add pyenv init to your shell
```shell
$ # zsh:
$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc
$ # or bash:
$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
```

Make sure to restart your shell so changes are applied
```shell
$ exec "$SHELL"
```

Optionally, you can install further dependencies (recommended)
```shell
$ brew install openssl readline sqlite3 xz zlib
```

Now install the required Python version

```shell
$ pyenv install 3.8.7
```

When running Python via pyenv, you might get an error such as:
```shell
$ python
version `3.8.7' is not installed (set by /some-path/image-processing/.python-version)
```
This could mean that the recommended Python version for this repository has been changed and you don't yet have it installed. 
You can easily install it using ```pyenv install [version]```. You will also have to recreate your virtual environment.

How to check the Python version used in the repository
```shell
$ cd image-processing
$ python --version
Python 3.7.10
```

You can read more about the installation at https://github.com/pyenv/pyenv#homebrew-on-macos

As a side note, you can also set a version system-wide (not recommended)
```shell
$ pyenv install 3.8.7
$ pyenv global 3.8.7
$ cd some-random-dir
$ python --version
Python 3.8.7
$ # but this will not affect the local version
$ cd image-processing
$ python --version
Python 3.7.10
```

# Guide for ultimate repository setup with Autoenv

If you follow these steps, every time you cd in the repo, the virtual env
will be automatically launched. When you leave it, it'll be deactivated :star:
```bash
git clone git://github.com/inishchith/autoenv.git ~/.autoenv
echo 'AUTOENV_ENABLE_LEAVE="aaa"  # Set to non-null string to enable this' | cat - ~/.autoenv/activate.sh > temp && mv temp ~/.autoenv/activate.sh
$ # zsh:
$ echo 'source ~/.autoenv/activate.sh' >> ~/.zshrc
$ # or bash:
$ echo 'source ~/.autoenv/activate.sh' >> ~/.bash_profile

```

All done! Now when you cd to the repo the virtual environment settings should be applied
automatically!
