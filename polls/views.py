from django.urls import reverse
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# Create your views here.
class IndexView(generic.ListView):
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # context = {"latest_question_list": latest_question_list}
    # return render(request,"polls/index.html",context);
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    

class DetailView(generic.DetailView):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, "polls/detail.html",{"question":question});
    model = Question
    template_name = "polls/detail.html"

    def get_queryser(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, "polls/results.html", {"question": question})
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request, "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
    )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))