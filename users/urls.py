from django.urls import path
from . views import *

urlpatterns = [
    path("addtocart/<uid>/",add_to_cart ,name="addtocart"),
    path("addtocarts/<uid>/",add_to_carts ,name="addtocarts"),
    path("showcart/", show_to_cart, name="showcart"),
    path("users/removecart/<uid>/", remove_cart_item, name="removecart"),
    path("mybook/", my_book, name="mybook"),
    path("bokingitem/<uid>/<h_uid>/", booking_item, name="bookingitem"),
    path('esewaform/', EsewaView.as_view(), name="esewaform"),
    path('esewaverify/<int:h_uid>/<int:b_uid>', esewa_verify, name="esewaverify"),
    path("profile/", profile, name="profilefff"),
    path("updateprofile/", update_profile, name="updateprofile"),
    # path('bokingitem/<uuid:uid>/<uuid:h_uid>/', booking_item, name='bookingitem'),
]