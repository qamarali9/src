from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.

from .models import UserProfile

User = get_user_model()

class UserProfileTestCase(TestCase):
	def setUp(self):
		self.username = "WhySoSerious?" 
		some_random_user = User.objects.create(username=self.username)

	def test_profile_created(self):
		userProfile = UserProfile.objects.filter(user__username=self.username)
		self.assertTrue(userProfile.exists())
		self.assertTrue(userProfile.count() == 1)

	def test_new_user(self):
		new_user = User.objects.create(username=self.username+"skhdcfk")