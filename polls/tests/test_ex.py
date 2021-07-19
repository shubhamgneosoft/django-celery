import sys

from django.urls import reverse
from django.utils import timezone

sys.path.append("..")

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from polls.models import Question


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_index(client):

    url = reverse('polls:index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail(client):
    question = Question.objects.create(
        question_text='test',
        pub_date=timezone.now()
       )
    url = reverse('polls:detail', kwargs={'question_id': question.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_results(client):
    question = Question.objects.create(
        question_text='test',
        pub_date=timezone.now()
       )
    url = reverse('polls:results', kwargs={'question_id': question.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthorized(client):
    url = reverse('polls:index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.fixture()
def fixture_func():
    print("fixture")
    return 1


def test_one(fixture_func):
    print("test1")
    assert 1 == 1


def test_two(fixture_func):
    assert 1 == 1

#
# @pytest.mark.django_db
# def test_my_user():
#     question = get_object_or_404(Question, pk=1)
#     print(question.question_text)
#     assert True
