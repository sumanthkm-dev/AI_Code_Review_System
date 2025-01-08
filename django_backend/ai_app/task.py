from utils.github import analyse_pr
from celery import Celery
from celery import shared_task

import eventlet

eventlet.monkey_patch()

app = Celery("django_backend")
app.config_from_object("django.conf.settings", namespace="CELERY")


@shared_task
def analyse_repo_task(repo_url, pr_number, github_token=None):
    result = analyse_pr(repo_url, pr_number, github_token)
    return result
