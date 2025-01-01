from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Amenities(BaseModel):
    amenity_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.amenity_name



class Hotel(BaseModel):
    hotel_name= models.CharField(max_length=100)
    hotel_price = models.IntegerField()
    description = models.TextField()
    hotel_url = models.URLField(null=True)
    phone = models.TextField(null=True, max_length=30)
    address = models.TextField(null=True)
    amenities = models.ManyToManyField(Amenities)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # services = models.ForeignKey(Services, on_delete=models.CASCADE, null=True)
    room_count = models.IntegerField(default=10)

    def __str__(self) -> str:
        return self.hotel_name


class HotelImages(BaseModel):
    hotel= models.ForeignKey(Hotel ,related_name="images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="static/hotels")

class HotelCart(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amenities = models.ManyToManyField(Amenities)
    created_at = models.DateTimeField(auto_now_add=True)

class HotelBooking(BaseModel):
    PAYMENT = {
        ('Cash on delivery', 'Cash on delivery'),
        ('Esewa', 'Esewa'),
    }
    hotel= models.ForeignKey(Hotel, related_name="hotel_bookings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_bookings", on_delete=models.CASCADE)
    booking_days= models.IntegerField(null=True)
    booking_room= models.IntegerField(null=True)
    total_price = models.PositiveIntegerField(null=True)
    contact_no = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    emailaddress = models.EmailField(null=True)
    payment_method = models.CharField(choices=PAYMENT, max_length=200, null=True)
    status = models.CharField(default='Pending', max_length=200,null=True)
    payment_status = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"Booking for {self.emailaddress}"

class UserProfile(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    frist_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=254, null=True)
    gender = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)
    profile_picture = models.ImageField(upload_to="static/uploadProfile",blank=True, null=False)
    Citizen_front = models.ImageField(upload_to='static/UploadCitizen', blank=True, null=False, default="Unknown")
    Citizen_back = models.ImageField(upload_to='static/UploadCitizen', blank=True, null=False, default="Unknown")
    accountType = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.user.username