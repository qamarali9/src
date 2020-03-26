from django.conf import settings
from django.db import models
# from django.core.exceptions import ValidationError
from .validators import validate_content
from django.urls import reverse_lazy
from django.utils import timezone

from django.db.models.signals import post_save

import re

from hashtags.signals import parsed_hashtags

# Create your models here.

# def validate_content(value):
# 		if value == "IND":
# 			raise ValidationError("Content can't be IND, me don't likey (via a validator function)")
# 		return value

class TweetModelManager(models.Manager):
	def retweet(self, user, parent_obj):
		if parent_obj.parent:
			parent_obj = parent_obj.parent

		qs = self.get_queryset().filter(
			user=user, parent=parent_obj).filter(
				timestamp__year=timezone.now().year,
				timestamp__month=timezone.now().month,
				timestamp__day=timezone.now().day,
			)
		if qs.exists():
			return None

		obj = self.model(
				parent = parent_obj,
				user = user,
				content = parent_obj.content,
			)
		obj.save()

		return obj

	def like_toggle(self, user, tweet_obj):
		if user in tweet_obj.liked.all():
			is_liked = False
			tweet_obj.liked.remove(user)
		else:
			is_liked = True
			tweet_obj.liked.add(user)
		return is_liked


class Tweet(models.Model):
	parent 		= models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	liked		= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
	content 	= models.CharField(max_length=140, validators=[validate_content])
	updated		= models.DateTimeField(auto_now=True)
	timestamp	= models.DateTimeField(auto_now_add=True)
	reply		= models.BooleanField(verbose_name="Is it a reply?", default=False)

	objects = TweetModelManager()

	def __str__(self):
		return str(self.content)

	def get_absolute_url(self):
		return reverse_lazy("tweets:detail",kwargs={"pk":self.pk})

	class Meta:
		ordering = ['-timestamp','content']

	# def clean(self, *args, **kwargs):
	# 	content = self.content
	# 	if content == "IND":
	# 		raise ValidationError("Content can't be IND, me don't likey")
	# 	return super(Tweet, self).clean(*args,**kwargs)

def post_save_tweet_receiver(sender, instance, created, *args, **kwargs):
	if created and not instance.parent:
		user_regex = r'@(?P<username>[\w.@+-]+)'
		usernames = re.findall(user_regex, instance.content)
		print(usernames)

		hashtag_regex = r'#(?P<hashtag>[\w\d-]+)'
		hashtags = re.findall(hashtag_regex, instance.content)
		print(hashtags)
		parsed_hashtags.send(sender=instance.__class__,hashtag_list=hashtags)

post_save.connect(post_save_tweet_receiver, sender=Tweet)