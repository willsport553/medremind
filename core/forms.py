import string
from django import forms
from django.core.exceptions import ValidationError
from .models import *


class PatientSetupForm(forms.Form):
    template_name = "core/form_template.html"

    nhi = forms.CharField(min_length=7, max_length=57, label="NHI",
                                    help_text="Enter your NHI number")

    def clean_nhi(self):
            cleaned_data = super().clean()
            nhi_key = cleaned_data['nhi_key']


            # Check the code is formatted correctly
            if not nhi_key.startswith(string, max_length=3):
                raise ValidationError("NHI must start with 'three letters'.")
            if not len(nhi_key) == 7:
                raise ValidationError("Please include the full 7 characters")

            # Check that the nhi hasn't already been used
            elif User.objects.filter(nhi=nhi_key).exists():
              raise ValidationError("Sorry, this NHI number is already in use.")
            return nhi_key