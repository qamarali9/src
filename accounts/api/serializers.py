from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import serializers

User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
	# follower_count = serializers.SerializerMethodField()
	url = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			# 'follower_count',
			'url'
		]

	# def get_follower_count(self,obj):
	# 	print("In Serializer : " + obj.username)
	# 	return 1

	def get_url(self,obj):
		return reverse_lazy("profiles:detail", kwargs={"username":obj.username})