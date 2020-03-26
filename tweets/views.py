from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View

from .forms import TweetModelForm
from .models import Tweet
from .mixins import FormUserNeededMixin, UserOwnerMixin

# Create your views here.

# Create
class TweetCreateView(FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = "tweets/create_view.html"
	#success_url = "/tweet/"

# NOTE : You don’t even need to provide a success_url for CreateView (or UpdateView) - 
# they will use get_absolute_url() on the model object if available.

	# def form_valid(self, form):
	# 	if self.request.user.is_authenticated:
	# 		form.instance.user = self.request.user
	# 		return super().form_valid(form)
	# 	else:
	# 		form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in."])
	# 		return self.form_invalid(form)

# def tweet_create_view(request):
# 	form = TweetModelForm(request.POST or None)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.user = request.user
# 		instance.save()

# 	context = {
# 		"form" : form 
# 	}
# 	return render(request,"tweets/create_view.html",context)


#Retrieve
class TweetDetailView(DetailView):
	#template_name = "tweets/detail_view.html"
	model = Tweet

	# def get_object(self):
	# 	pk = self.kwargs.get("pk")
	# 	return get_object_or_404(Tweet, id=pk)

class TweetListView(LoginRequiredMixin, ListView):
	#template_name = "tweets/list_view.html"
	#model = Tweet

	def get_queryset(self,*args,**kwargs):
		qs = Tweet.objects.all()
		query = self.request.GET.get("q",None)
		if query is not None:
			qs = qs.filter(
				    Q(content__icontains=query) |
				    Q(user__username__icontains=query)
				)
		return qs

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['now'] = timezone.now()
		context['create_form'] = TweetModelForm()
		context['create_url'] = reverse_lazy("tweets:create")
		#print(context)
		return context

# def tweet_detail_view(request,pk=None):
# 	# obj = Tweet.objects.get(pk=pk)
# 	obj = get_object_or_404(Tweet, pk=pk)
# 	print(obj)
# 	context = {
# 		"object" : obj
# 	}
# 	return render(request,"tweets/detail_view.html",context)

# def tweet_list_view(request):
# 	queryset = Tweet.objects.all()
# 	print(queryset)
# 	for obj in queryset:
# 		print(obj.content)
# 	context = {
# 		"object_list" : queryset
# 	}
# 	return render(request,"tweets/list_view.html",context)


#Update
class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
	model = Tweet
	form_class = TweetModelForm
	template_name = "tweets/update_view.html"
	success_url = reverse_lazy("tweets:home")


#Delete
class TweetDeleteView(LoginRequiredMixin, DeleteView):
	model = Tweet
	template_name = "tweets/delete_confirm.html"
	success_url = reverse_lazy("tweets:home")

class RetweetView(View):
	def get(self, request, pk, *args, **kwargs):
		tweet = get_object_or_404(Tweet, pk=pk)
		if request.user.is_authenticated:
			new_tweet = Tweet.objects.retweet(request.user,tweet)
			return HttpResponseRedirect("/")
		return HttpResponseRedirect(tweet.get_absolute_url())