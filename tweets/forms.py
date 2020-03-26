from django import forms

from .models import Tweet

class TweetModelForm(forms.ModelForm):
	# content = forms.CharField(label="", 
	# 	widget=forms.Textarea(
	# 		attrs={"placeholder":"Your message.", 
	# 			"class":"form-control"}
	# 		)
	# 	)
	class Meta:	
		model = Tweet
		fields = [
			"content",
		]
		#exclude=["user"]

	# def clean_content(self):
	# 	content = self.cleaned_data["content"]
	# 	if content == "IND":
	# 		raise forms.ValidationError("Can't be IND, me don't likey")
	# 	return clean_content