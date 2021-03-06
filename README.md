Mixxx Backstage is a community portal where Mixxx users can share Mixxx customizations.

Server Setup
============

```shell
# Generally useful stuff.
sudo apt-get install emacs23-nox emacs-goodies-el ack-grep htop zsh git tmux screen
# C/C++ Compiler.
sudo apt-get install build-essential
# Python packages and development headers.
sudo apt-get install python-dev python-virtualenv python-setuptools python-pip
# Postgres and development headers.
sudo apt-get install postgresql-9.1 postgresql-server-dev-9.1
````

Environment Setup
=================

```shell
git clone git@github.com:mixxxdj/backstage.git
cd backstage
virtualenv --distribute ./virtualenv
source virtualenv/bin/activate
# You should see the (virtualenv) tag in your prompt now.
pip install django
pip install psycopg2
```

Running a development server
============================

This works as it usually does with Django:

```shell
python manage.py runserver host:port
```

Then navigate to http://host:port/.
