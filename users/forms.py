from django import forms
from publice .models import *

class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ["booking_days", "contact_no", "address","emailaddress", "payment_method", "booking_room"]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [ "frist_name", "last_name", "email", "contact_number", "address","gender", "profile_picture"]


class BookingForm(forms.Form):
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
    contact_no = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    emailaddress = forms.EmailField(required=True)
    payment_method = forms.ChoiceField(
        choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')],
        required=True
    )
    booking_room = forms.CharField(max_length=100, required=True)