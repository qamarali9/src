from django.core.exceptions import ValidationError

def validate_content(value):
		if value == "IND":
			raise ValidationError("Content can't be IND, me don't likey (via a validator function)")
		return value