from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from .models import UserProfile
from .forms import UserRegisterForm

# Create your views here.

User = get_user_model()


class UserRegistrationView(FormView):
	template_name = 'accounts/user_register_form.html'
	form_class = UserRegisterForm
	success_url = '/accounts/login'

	def form_valid(self, form):
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		new_user = User.objects.create(username=username,email=email)
		new_user.set_password(password)
		new_user.save()
		return super().form_valid(form)

class UserDetailView(DetailView):
	queryset = User.objects.all()
	template_name = "accounts/accounts_detail.html"

	def get_object(self):
		return get_object_or_404(User, username__iexact=self.kwargs.get("username"))
	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(*args,**kwargs)
		context['following'] = UserProfile.objects.is_following(self.request.user, self.get_object())
		context['recommended'] = UserProfile.objects.recommended(self.request.user)
		# print(context['recommended'])
		return context



class UserFollowView(View):
	def get(self, request, username, *args, **kwargs):
		toggle_user = get_object_or_404(User, username__iexact=username)
		if request.user.is_authenticated:
			is_added = UserProfile.objects.toggle_follow(request.user,toggle_user)
		return redirect("profiles:detail", username=username)