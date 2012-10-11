#!/bin/bash
# this is an easy (re)deploy script for running a lflux instance w/ pbundler, gunicorn and supervisord

pbundle # update dependencies.
pbundle run ./manage.py collectstatic --noinput
pbundle run ./manage.py migrate
pbundle run printenv SUPERVISOR_NAME
pbundle run sudo supervisorctl restart `printenv SUPERVISOR_NAME`