from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class InputForm(forms.Form):
    validate_expression = RegexValidator(r'^[0-9\.+\-*/()]*$', 'Invalid Output.')
    input = forms.CharField(validators=[validate_expression], max_length=100)

    def clean_input(self):
        data = self.cleaned_data['input']
        # Removes whitespace
        data = ''.join(data.split())
        return data
