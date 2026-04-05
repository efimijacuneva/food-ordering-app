from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Order

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")
    phone = forms.CharField(max_length=15, required=True, label="Phone Number")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) < 7:
            raise forms.ValidationError("Phone number is too short.")
        return phone

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['guest_email', 'guest_phone']
        widgets = {
            'guest_email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'guest_phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and self.request.user.is_authenticated:
            self.fields.pop('guest_email')
            self.fields.pop('guest_phone')

class GuestOrderForm(forms.Form):
    email = forms.EmailField(required=True, label="Email Address")
    phone = forms.CharField(max_length=15, required=True, label="Phone Number")