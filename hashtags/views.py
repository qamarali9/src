from django.shortcuts import render
from django.views import View

from .models import HashTag
# Create your views here.

class HashTagView(View):
	def get(self, request, hashtag, *args, **kwargs):
		obj, created = HashTag.objects.get_or_create(tag=hashtag)
		return render(request,"hashtags/tag_view.html",{"obj":obj})