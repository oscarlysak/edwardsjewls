from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'forminputdiv rounding dropshadow5',
        'placeholder': 'Enter',
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'forminputdiv rounding dropshadow5',
        'placeholder': 'Enter',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'forminputdiv rounding dropshadow5',
        'placeholder': 'Enter',
    }))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'forminputdiv rounding dropshadow5',
        'placeholder': 'Enter',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'forminputdiv rounding dropshadow5',
        'placeholder': 'Enter Your Message Here',
    }))
