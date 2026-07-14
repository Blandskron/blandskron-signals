from django import forms

from .models import Subscriber


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email", "weekly_digest", "artificial_intelligence", "development", "automation", "business_technology", "featured_analysis_only"]
        widgets = {"email": forms.EmailInput(attrs={"placeholder": "tu@email.com", "autocomplete": "email"})}
