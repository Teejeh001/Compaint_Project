from django import forms
from .models import Student, Complaint

class StudentSignupForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['fullname', 'matric_no', 'email']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'matric_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matric Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }



class ComplaintForm(forms.ModelForm):
    matric_no = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Matric Number'})
    )

    class Meta:
        model = Complaint
        fields = ['matric_no', 'title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Complaint Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your complaint', 'rows': 4}),
        }


class AdminResponseForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['admin_response', 'status']
        widgets = {
            'admin_response': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your response here'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
