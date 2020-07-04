# forms.py
from django import forms
from .models import StudentForm1  # models.py


class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentForm1
        fields = "__all__"