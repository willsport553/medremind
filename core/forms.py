import re
import string
from django import forms
from django.core.exceptions import ValidationError
from .models import *


class PatientSetupForm(forms.Form):
    template_name = "core/form_template.html"

    nhi_key = forms.CharField(min_length=7, max_length=57, label="NHI",
                                    help_text="Enter your NHI number")

    def clean_nhi_key(self):
            cleaned_data = super().clean()
            nhi_key = cleaned_data['nhi_key']


            # Check the code is formatted correctly
            if (re.search(r"[A-Z]{3}[0-9]{4}", nhi_key) == None):
                raise ValidationError("NHI must be of 3 uppercase letter folowed by 4 numbers")
            if not len(nhi_key) == 7:
                raise ValidationError("Please include the full 7 characters")

            # Check that the nhi hasn't already been used
            elif Patient.objects.filter(nhi=nhi_key).exists():
              raise ValidationError("Sorry, this NHI number is already in use.")
            return nhi_key