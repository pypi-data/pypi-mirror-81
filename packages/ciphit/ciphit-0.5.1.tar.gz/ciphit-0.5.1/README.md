<p align="center">
    <a href="https://github.com/sgrkmr/ciphit", alt="ciphit">
        <img src="https://user-images.githubusercontent.com/57829219/84270533-7492e380-ab48-11ea-9270-8531ea72ac6e.png", alt="ciphit">
    </a>
</p>
<p align="center">
    <a href="https://GitHub.com/sgrkmr/ciphit/releases/", alt="version">
        <img src="https://img.shields.io/github/release/sgrkmr/ciphit.svg?style=flat-square&color=blue", alt="version">
    </a>
    <a href="https://GitHub.com/sgrkmr/ciphit/releases/", alt="downloads">
        <img src="https://img.shields.io/github/downloads/sgrkmr/ciphit/total.svg?style=flat-square", alt="downloads">
    </a>
    <a href="https://github.com/sgrkmr/ciphit/commits/master", alt="commit">
        <img src="https://img.shields.io/github/last-commit/sgrkmr/ciphit?style=flat-square", alt="commit">
    </a>
    <a href="https://www.python.org/downloads/release/python-374/">
        <img src="https://img.shields.io/badge/Python-3.7-blue?style=flat-square", alt="python3">
    </a>
    <a href="https://GitHub.com/sgrkmr/ciphit/graphs/contributors/", alt="contributors">
        <img src="https://img.shields.io/github/contributors/sgrkmr/ciphit.svg?style=flat-square", alt="contributors">
    </a>
    <a href="https://opensource.org/licenses/MIT" alt="license">
    <img src="https://img.shields.io/github/license/sgrkmr/ciphit.svg?style=flat-square", alt="license">
    </a>
</p>

<p align="center">
<code>ciphit</code> is a basic cryptography cli-tool, Currently only supports AES-CBC.
</p>

---
<!--
# Screenshots
![scrn](https://user-images.githubusercontent.com/57829219/84272798-81fd9d00-ab4b-11ea-89e2-c712a16c00a3.png)
-->
## Prerequisites
* Packages:
    * cryptography`>=2.8`
    * rich`>=8.0.0`
    * click`>=7.1.2`
    * click-option-group`>=0.5.1`

## Installation
On shell run this command:
 ```bash
 $ python3 -m pip install ciphit --upgrade
 ```
Or
To install `ciphit` directly from source, you have to clone the repo and checkout to `./ciphit`
 ```bash
 $ git clone https://github.com/sgrkmr/ciphit.git
 $ cd ciphit
 ```
Now, you may install `ciphit` via either of these two commands:
 ```bash
 $ pip install .
 ```
 ```bash
 $ python setup.py install
 ```
`ciphit` is now installed.<br/>for eg. to show the `help` message, use:
 ```bash
 $ ciphit --help
 ```
<p><b>Make sure you run these commands in Terminal/CMD or any other shell you use.</b></p>

## License
Licensed under [MIT](https://opensource.org/licenses/MIT).
