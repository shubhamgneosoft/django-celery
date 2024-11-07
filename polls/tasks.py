# from __future__ import absolute_import, unicode_literals
import time

from celery import shared_task
from django.http import request
from django.shortcuts import get_object_or_404

from .models import Question, Choice


@shared_task
def add(x, y):
    z = x + y
    print(z)
    return z


@shared_task
def add_vote(question_id, choice):
    time.sleep(10)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=choice)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        print(None)
    else:
        selected_choice.votes += 1
        selected_choice.save()
