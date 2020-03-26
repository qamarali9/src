from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView

from rest_framework.response import Response

from .serializers import TweetModelSerializer
from .pagination import StandardResultsSetPagination

from tweets.models import Tweet
from django.db.models import Q

class LikeAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, pk, format=None):
		tweet_qs = Tweet.objects.filter(pk=pk)
		message = "Not allowed"
		if request.user.is_authenticated:
			is_liked = Tweet.objects.like_toggle(request.user,tweet_qs.first())
			return Response({"liked":is_liked})
		return Response({"message":message},status=400)


class RetweetAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, pk, format=None):
		tweet_qs = Tweet.objects.filter(pk=pk)
		message = "Not allowed"
		if tweet_qs.exists() and request.user.is_authenticated:
			new_tweet = Tweet.objects.retweet(request.user,tweet_qs.first())
			if new_tweet is not None:
				data = TweetModelSerializer(new_tweet).data
				return Response(data)
			message = "Can not retweet the same tweet within a day"
		return Response({"message":message},status=400)


class TweetCreateAPIView(generics.CreateAPIView):
	serializer_class = TweetModelSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)


class TweetDetailAPIView(generics.ListAPIView):
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultsSetPagination
	permission_classes = [permissions.AllowAny]

	def get_queryset(self,*args,**kwargs):
		pk = self.kwargs.get("pk")
		obj = Tweet.objects.get(pk=pk)
		if obj.parent:
			obj = obj.parent
		qs1 = Tweet.objects.filter(pk=obj.pk)
		qs2 = Tweet.objects.filter(parent=obj)
		return (qs1 | qs2).distinct().extra(select={"parent_id_null":"parent_id IS NULL"}).order_by("-parent_id_null","-timestamp")


class SearchAPIView(generics.ListAPIView):
	queryset = Tweet.objects.all().order_by("-timestamp")
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultsSetPagination

	def get_serializer_context(self,*args,**kwargs):
		context = super().get_serializer_context()
		context["request"] = self.request
		return context

	def get_queryset(self, *args, **kwargs):
		qs = self.queryset
		query = self.request.GET.get("q",None)
		if query is not None:
			qs = qs.filter(
				    Q(content__icontains=query) |
				    Q(user__username__icontains=query)
				)
		return qs


class TweetListAPIView(generics.ListAPIView):
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultsSetPagination

	def get_serializer_context(self,*args,**kwargs):
		context = super().get_serializer_context()
		context["request"] = self.request
		return context

	def get_queryset(self,*args,**kwargs):
		requested_user = self.kwargs.get("username")
		if requested_user:
			qs = Tweet.objects.filter(user__username=requested_user).order_by("-timestamp")
		else:
			im_following = self.request.user.profile.get_following()
			qs1 = Tweet.objects.filter(user__in=im_following)
			qs2 = Tweet.objects.filter(user=self.request.user)
			qs = (qs1 | qs2).distinct().order_by("-timestamp")
		# print(self.request.GET)
		print("In TweetListAPIView get_queryset method : request =" + str(self.request.GET))
		query = self.request.GET.get("q",None)
		if query is not None:
			qs = qs.filter(
				    Q(content__icontains=query) |
				    Q(user__username__icontains=query)
				)
		return qs