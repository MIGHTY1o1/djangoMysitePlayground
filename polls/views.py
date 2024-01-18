from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from .models import Question, Choice
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import JsonResponse


# //==========================index==================================//


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # Assuming you want to serialize a list of questions to JSON
    serialized_data = [
        {"question_text": question.question_text, "pub_date": question.pub_date}
        for question in latest_question_list
    ]
    # Returning JsonResponse with serialized data
    return JsonResponse(serialized_data, safe=False)


# defs for index view
{
    # def index(request):
    #     latest_question_list = Question.objects.order_by("-pub_date")[
    #         :5
    #     ]  # this line is reponsible to fetch the data from db
    #     template = loader.get_template("polls/index.html")
    #     context = {
    #         "latest_question_list": latest_question_list,
    #     }
    #     return HttpResponse(template.render(context, request))
    # second method
    # def index(request):
    #     latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #     context = {"latest_question_list": latest_question_list}
    #     return render(request, "polls/index.html", context)
    # 4th way, return res as json
    # def index(request):
    #     latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #     # Assuming you want to serialize a list of questions to JSON
    #     serialized_data = [
    #         {"question_text": question.question_text, "pub_date": question.pub_date}
    #         for question in latest_question_list
    #     ]
    #     # Returning JsonResponse with serialized data
    #     return JsonResponse(serialized_data, safe=False)
}
# //======================================================================//


# we added some more views here
# //===============================detail=======================================//
# detail
# using genric views
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     return Question.objects.filter(pub_date__lte=timezone.now())
    def detail(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, "polls/detail.html", {"question": question})


# defs for detail view
{
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
}
# //======================================================================//


# //===============================results=======================================//
# results
# using generic views
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


{  # def results(request, question_id):
    #     question = get_object_or_404(Question, pk=question_id)
    #     return render(request, "polls/results.html", {"question": question})
}

# //======================================================================//


# //==============================votes========================================//
# votes
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
