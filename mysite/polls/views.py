

# Create your views here.

from typing import Any
from django.db import models
from django.http import HttpResponse,HttpResponseRedirect
from .models  import Questions,Choice
from django.shortcuts import render

from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from django.views import generic

# def index(request,question_id):

	

# 	try:
# 		question=Questions.objects.get(pk=question_id)
# 	except Questions.DoesNotExist:
# 		raise Http404("Questions does not exist")
# 	return render(request,"polls/index.html",{"question":question})

    
# 	# latest_queston_list=Questions.objects.order_by("-pub_date")[:5]
# 	# output = ",".join([q.question_text for q in latest_queston_list])
# 	# return HttpResponse(output)

# 	# latest_question_list = Questions.objects.order_by("-pub_date")[:5]
# 	# template=loader.get_template("polls/index.html")
# 	# context={"latest_question_list":latest_question_list}
# 	# return render(request,"polls/index.html",context)
	
# 	#or


# 	# return HttpResponse(template.render(context,request))
	


# def detail(request,question_id):
# 	question=get_object_or_404(Questions,pk=question_id)

# 	# return HttpResponse("You are looking at question %s",question_id)
# 	return render(request,"polls/detail.html",{"question":question})

# def results(request,question_id):
# 	question=get_object_or_404(Questions,pk=question_id)
# 	return render(request,"polls/results.html",{"question":question})
	

class IndexView(generic.ListView):
	template_name="polls/index.html"
	context_object_name="latest_question_list"

	def get_queryset(self):
		'''return Questions.objects.order_by("-pub_date")[:5]'''
		return Questions.objects.filter(pub_date=timezone.now()).order_by("pub_date")[:5]
	
    
	
class DetailView(generic.DetailView):
	model=Questions
	context_object_name="question"
	template_name="polls/detail.html"

	def get_queryset(self) :
		return Questions.objects.filter(pub_date=timezone.now())

class ResultsView(generic.DetailView):
	model=Questions
	context_object_name="question"

	template_name="polls/results.html"
		

def vote(request,question_id):
	question=get_object_or_404(Questions,pk=question_id)
	try:
		selected_choice=question.choice_set.get(pk=request.POST["choice"])

	except(KeyError,Choice.DoesNotExist):
		return render(request,"polls/detail.html",{
			"question":question,
			"error_message":"You didn't select a choice",
		},
		)
	else:
		selected_choice.votes+=1
		selected_choice.save()
		return HttpResponseRedirect(reverse("polls:results",args=[question_id],))
