from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from .models import Question, Choice
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# //==========================2 ways render template in django==================================//
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[
#         :5
#     ]  # this line is reponsible to fetch the data from db
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


# third way to use generic view
# class IndexView(generic.ListView):
#     template_name = "polls/index.html"
#     context_object_name = "latest_question_list"


# def get_queryset(self):
#     """
#     Return the last five published questions (not including those set to be
#     published in the future).
#     """
#     return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
#         :5
#     ]


# we added some more views here
# //===============================detail=======================================//
# detail
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# return detail.html
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "polls/detail.html", {"question": question})


# shortcut to throw 404 if objec!=true
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


# using genric views
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# //======================================================================//


# //===============================results=======================================//
# results
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})


# using generic views
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# //======================================================================//


# //==============================votes========================================//
# votes
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
# returning the acutal vote count and saving it to db
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# //======================================================================//
