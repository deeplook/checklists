Checklist: Making a Release (WIP)
=================================

.. tags:

    meta info version tag documentation code repository pypi code fix build test publish announce


Assumptions
-----------

- the code base has a well-defined structure
- the code is packaged using setup.py
- it is under version control, e.g. git, hg
- it has a testsuite
- it has documentation
- all is hosted in a remote repository, e.g. on github/bitbucket


Versioning info
---------------

- ensure something like PROJECT/version.py contains the desired version number
- ensure README.rst contains the right version number
- ensure version in docs/manual/conf.py is up-to-date


Meta info
----------

- ensure AUTHORS.txt, CHANGELOG.txt and LICENSE.txt exist and are up-to-date
- ensure README.rst contains the right info (version, examples...)


Build documentation
-------------------

- update version in docs/manual/conf.py
- ensure docs/manual/\*.txt contains the right info (version, examples...)
- run make_docs.sh and check output in docs/manual/_build/html

Tools: sphinx


Scan local code
---------------

- search for ##TODO and ##FIXME labels and handle as needed
- check for open issues on github/bitbucket and handle as needed

Tools: grep


Test local code
---------------

- ensure that any necessary hardware used in the tests is running correctly

- tox
- run python setup.py install
- run py.test tests/test\_\*.py with whatever restrictions needed
- run python demos/\*.py with whatever restrictions needed 
- create coverage report

- run python setup.py sdist
- unpack created dist/PROJECT-XXX archive
- verify it contains what it should and doesn't what it doesn't
- test different installation types in virtualenvs (listed in a seperate file)

Tools: py.test, tox, coverage


Upload code repository to hoster
--------------------------------

- commit all changes to local repository
- push all changes to remote hoster
- create a release package on remote hoster 
- test installation from remote hoster

Tools: git, hg, pip


Upload code on pypi
-------------------

- ensure ~/.pypirc contains the name and password for the pypi PROJECT account
- run python setup.py sdist upload
- make a tag on github/bitbucket for the current release

Tools: python, git, hg


Disemminate documentation
-------------------------

- update docs on PROJECT.readthedocs.org (pulled from github/bitbucket)
- adapt documentation maintained on some other site as needed

Tools: rtfd api, http://read-the-docs.readthedocs.org/en/latest/api.html


Announce release
----------------

- PROJECT newsletter
- comp.lang.python
- comp.lang.python.announce
- twitter
- ...

Tools: email, blog, twitter, ...
  

Further inspiration
-------------------

Search for "python release checklist" with your favourite search engine...

- https://gist.github.com/audreyr/5990987
- https://github.com/pydata/pandas/wiki/Release-Checklist
- https://github.com/oisin/app-release-checklist/blob/master/checklist.md
- https://pythonhosted.org/mrs-mapreduce/release_checklist.html
- http://nipy.bic.berkeley.edu/nightly/nibabel/doc/devel/make_release.html
