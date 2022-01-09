channels-easy
============

A thin wrapper around channel consumers to make things **EASY**.

Installation
------------

To get the latest stable release from PyPi

```bash
pip install channels-easy
```
To get the latest commit from GitHub

```bash
pip install -e git+git://github.com/namantam1/channels-easy.git#egg=channels-easy
```
<!-- TODO: Describe further installation steps (edit / remove the examples below): -->

Add ``channels-easy`` to your ``INSTALLED_APPS``

```bash
INSTALLED_APPS = (
    ...,
    'channels-easy',
)
```
<!-- Add the ``channels-easy`` URLs to your ``urls.py``

```bash
urlpatterns = [
    url(r'^VAR_URL_HOOK/', include('channels-easy.urls')),
]
``` -->

Usage
-----

TODO: Describe usage or point to docs. Also describe available settings.


Contribute
----------

If you want to contribute to this project, please perform the following steps

````bash
# Fork this repository
# Clone your fork
poetry install

git checkout -b feature_branch master
# Implement your feature and tests
git add . && git commit
git push -u origin feature_branch
# Send us a pull request for your feature branch
````
<!-- In order to run the tests, simply execute ``tox``. This will install two new
environments (for Django 1.8 and Django 1.9) and run the tests against both
environments. -->
