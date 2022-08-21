from multiprocessing import context
from re import template
from urllib import request
from webbrowser import get
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
import random
from django.urls import reverse

def index(request):
        latest_questions = Question.objects.all()
        template = 'polls/index.html'
        context = {'latest_questions': latest_questions}
        return render(request, template, context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    n = range(1,10)
    template = 'polls/detail.html'
    context = {'question': question, 'n': n}
    return render(request, template, context)


def results(request, question_id):
    template = 'polls/results.html'
    question = get_object_or_404(Question, pk=question_id)
    return render(request, template, {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error': 'You didnt select a choice'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))