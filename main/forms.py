from django import forms
from django.core.validators import EmailValidator
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Contact form for the website"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'inquiry_type']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes and attributes to form fields
        self.fields['name'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Your full name',
            'required': True,
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'your.email@example.com',
            'required': True,
            'type': 'email',
        })
        
        self.fields['subject'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Subject of your message',
        })
        
        self.fields['message'].widget.attrs.update({
            'class': 'form-textarea',
            'placeholder': 'Write your message here...',
            'rows': 5,
            'required': True,
        })
        
        self.fields['inquiry_type'].widget.attrs.update({
            'class': 'form-select',
        })
        
        # Customize labels
        self.fields['name'].label = 'Full Name'
        self.fields['email'].label = 'Email Address'
        self.fields['subject'].label = 'Subject (Optional)'
        self.fields['message'].label = 'Your Message'
        self.fields['inquiry_type'].label = 'Inquiry Type'
        
        # Make subject optional
        self.fields['subject'].required = False
    
    def clean_email(self):
        """Validate email field"""
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator()
            validator(email)
        return email
    
    def clean_message(self):
        """Validate message field"""
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 10:
            raise forms.ValidationError('Please provide a more detailed message (at least 10 characters).')
        return message


class NewsletterForm(forms.Form):
    """Simple newsletter subscription form"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email address',
            'required': True,
        }),
        label='Email Address'
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator()
            validator(email)
        return email