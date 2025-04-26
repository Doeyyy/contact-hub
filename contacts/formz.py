from django import forms
from .models import Contact
from django.core.exceptions import ValidationError

class Contactform(forms.ModelForm):
    name = forms.CharField(
        # this allows u to customise the django form
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder':'Contact Name'
        })
    )

    email = forms.EmailField(
         widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder':'Email address'
        })
    )


    document = forms.FileField(
         widget=forms.FileInput(attrs={
            'class': 'file-input fiel-input-bordered input-bordered w-full',
            
        }),#we go to template to add it
        required= False #meaning we can optionally add a document but its not required by the frm class
    )


 

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Ensure user exists on instance before filtering
        if self.instance.pk:  # If editing an existing contact
            user = self.instance.user
        else:  # If creating a new contact
            user = self.initial.get('user')  # Get user from the form instance

        if user and Contact.objects.filter(user=user, email=email).exists():
            raise ValidationError("You already have this email in your contacts.")

        return email




    class Meta:
        model= Contact
        fields = (
            'name', 'email', 'document'
        )



