from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.test import TestCase

# Create your tests here.

from .models import Tweet

User = get_user_model()

class TestModelTestCase(TestCase):
	def setUp(self):
		some_random_user = User.objects.create(username="WhySoSerious?")

	def test_tweet_item(self):
		obj = Tweet.objects.create(
			user=User.objects.first(),
			content="Random content."
		)
		self.assertTrue(obj.content=="Random content.")
		self.assertEqual(obj.id,1)

	def test_tweet_url(self):
		obj = Tweet.objects.create(
			user=User.objects.first(),
			content="Random content."
		)
		absolute_url = reverse_lazy("tweets:detail",kwargs={"pk":obj.id})
		self.assertEqual(obj.get_absolute_url(),absolute_url)