from django import forms
from django.core.validators import validate_email


class MultiEmailField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for email in value:
            # print(email)
            validate_email(email)


class SendEmail(forms.Form):
    to = MultiEmailField(required=False)
    cc = MultiEmailField(required=False)
    bcc = MultiEmailField(required=False)
    subject = forms.CharField(max_length=1000000000, required=False)
    body = forms.CharField(widget=forms.Textarea, required=False)
