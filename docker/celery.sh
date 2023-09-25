#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery --app=app.tasks.celery_task:celery worker --loglevel=INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=app.tasks.celery_task:celery flower
fi