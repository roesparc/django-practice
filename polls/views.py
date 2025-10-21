from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from .models import Question, Choice
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    model = Question
    template_name = "polls/index.html"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        now = timezone.now()
        past_questions = Question.objects.filter(pub_date__lte=now)
        return past_questions.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        selected_choice = question.choice_set.get(pk=request.POST["choice"])

    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    except KeyError:
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )

    except Choice.DoesNotExist:
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Choice not found.",
            },
        )

    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
