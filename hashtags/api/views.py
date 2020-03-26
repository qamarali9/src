from rest_framework import generics

from tweets.api.serializers import TweetModelSerializer
from tweets.api.pagination import StandardResultsSetPagination

from tweets.models import Tweet
from hashtags.models import HashTag
from django.db.models import Q


class HashTagAPIView(generics.ListAPIView):
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultsSetPagination

	def get_serializer_context(self,*args,**kwargs):
		context = super().get_serializer_context()
		context["request"] = self.request
		return context

	def get_queryset(self, *args, **kwargs):
		hashtag = self.kwargs.get("hashtag",None)
		try:
			hashtag_obj, created = HashTag.objects.get_or_create(tag=hashtag)
		except:
			pass
		if hashtag_obj is not None:
			qs = hashtag_obj.get_tweets()
			query = self.request.GET.get("q",None)
			if query is not None:
				qs = qs.filter(
					    Q(content__icontains=query) |
					    Q(user__username__icontains=query)
					)
			return qs
		return None