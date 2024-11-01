from django import forms
from .models import DiaryEntry
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CalorieCalculatorForm(forms.Form):
    age = forms.IntegerField(label='Age', min_value=0)
    gender = forms.ChoiceField(label='Gender', choices=[('male', 'Male'), ('female', 'Female')])
    height = forms.FloatField(label='Height (cm)', min_value=0)
    weight = forms.FloatField(label='Weight (kg)', min_value=0)
    activity_level = forms.ChoiceField(
        label='Activity Level',
        choices=[
            ('sedentary', 'Sedentary (little or no exercise)'),
            ('light', 'Lightly active (light exercise/sports 1-3 days/week)'),
            ('moderate', 'Moderately active (moderate exercise/sports 3-5 days/week)'),
            ('active', 'Very active (hard exercise/sports 6-7 days a week)'),
            ('extra_active', 'Super active (very hard exercise/sports & physical job)')
        ]
    )

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['food_name', 'calories', 'protein', 'carbohydrates', 'fat', 'category']
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Email is already in use.')
        return email