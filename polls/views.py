from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Question, Choice
# from .tasks import add_vote


def index(request):
    """
    List out all questions
    :param request: request
    :return:
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """
    See the choices as per question id and select choice for vote
    :param request: request
    :param question_id: int
    :return: Html Response
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    """
    See the voting count as per the question
    :param request: request
    :param question_id: Int
    :return: Html Response
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    """
    Increase the vote count as per questions
    :param request: request
    :param question_id: Int
    :return: Http Response
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        print(request.POST['choice'])
        selected_choice = question.all_choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # add_vote.delay(question_id, request.POST['choice'])
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
