from django import forms
from publice .models import *

# class ReservationForm(forms.ModelForm):
#     class Meta:
#         model = Reservation
#         fields = ['check_in_date', 'check_out_date', 'number_of_guests']


class AmenitiesForm(forms.ModelForm):
    class Meta:
        model = Amenities
        fields = ['amenity_name']

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["hotel_name", "hotel_price", "description", "amenities", "room_count"]

class HotelImagesForm(forms.ModelForm):
    class Meta:
        model = HotelImages
        fields = ["hotel","images"]
