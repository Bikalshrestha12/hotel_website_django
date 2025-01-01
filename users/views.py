from django.shortcuts import render, redirect
from django.http import *
from publice.models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . auth import admin_only

# Create your views here.

@login_required
def add_to_cart(request, uid):
    user = request.user
    hotel = Hotel.objects.get(uid=uid)
    check_presence = HotelCart.objects.filter(user=user, hotel=hotel)
    if check_presence:
        messages.add_message(request, messages.ERROR, "Item is alreay present in cart")
        return redirect("/hotel_list")
    else:
        cart = HotelCart.objects.create(user=user, hotel=hotel)
        if cart:
            messages.add_message(request, messages.SUCCESS, "Item add successfully")
            return redirect("/users/showcart")
        else:
            messages.add_message(request, messages.ERROR, "Please try again")

@login_required
def add_to_carts(request, uid):
    user = request.user
    hotel = Hotel.objects.get(uid=uid)
    check_presence = HotelCart.objects.filter(user=user, hotel=hotel)
    if check_presence:
        messages.add_message(request, messages.ERROR, "Item is alreay present in cart")
        return redirect("/users/showcart")
    else:
        cart = HotelCart.objects.create(user=user, hotel=hotel)
        if cart:
            messages.add_message(request, messages.SUCCESS, "Item add successfully")
            return redirect("/users/showcart")
        else:
            messages.add_message(request, messages.ERROR, "Please try again")

@login_required
def show_to_cart(request):
    user = request.user
    item = HotelCart.objects.filter(user=user)
    context = {"item": item}
    return render(request, "users/mycart.html", context)


@login_required
def remove_cart_item(request, uid):
    item = HotelCart.objects.get(uid=uid)
    item.delete()
    messages.add_message(request, messages.ERROR, "Item removed successfully")
    return redirect("/users/showcart") 


# @login_required
# def booking_item(request, h_uid, uid):
#     user = request.user
#     cart = HotelCart.objects.get(uid=uid)
#     hotel = Hotel.objects.get(uid=h_uid)

#     if request.method == "POST":
#         form = HotelBookingForm(request.POST)
#         if form.is_valid():
#             start_date = request.POST.get("start_date")
#             end_date = request.POST.get("end_date")
#             price = hotel.hotel_price
#             booking_room = request.POST.get("booking_room")
#             total_price = int(price) * (int(end_date)-int(start_date)) * int(booking_room)
#             contact_no = request.POST.get("contact_no")
#             address = request.POST.get("address")
#             payment_method = request.POST.get("payment_method")
#             payment_status = request.POST.get("payment_status")
#             order = HotelBooking.objects.create(
#                 hotel=hotel,
#                 user=user,
#                 start_date=start_date,
#                 booking_room=booking_room,
#                 end_date=end_date,
#                 total_price=total_price,
#                 contact_no=contact_no,
#                 address=address,
#                 payment_method=payment_method,
#                 payment_status=payment_status,
#             )
#             if order.payment_method == "Cash on delivery":
#                 item = HotelCart.objects.get(uid=uid)
#                 item.delete()
#                 messages.add_message(
#                     request, messages.SUCCESS, "Booking Successfull be ready with Cash"
#                 )
#                 return redirect("/users/mycart")
#             # elif order.payment_method == "Esewa":
#             #     return redirect(
#             #         reverse("esewaform")
#             #         + "?o_id="
#             #         + str(order.id)
#             #         + "&c_id="
#             #         + str(cart.id)
#             #     )
#             else:
#                 messages.add_message(
#                     request, messages.ERROR, "Kindly check the payment method"
#                 )
#                 return render(request, "publice/hotel_list.html", {"form": form})

#     context = {"form": HotelBookingForm}
#     return render(request, "users/bookingform.html", context)

from datetime import datetime
from django.urls import reverse
from urllib.parse import urlencode
import decimal

@login_required
def booking_item(request, h_uid, uid):
    user = request.user
    cart = HotelCart.objects.get(uid=uid)
    hotel = Hotel.objects.get(uid=h_uid)

    if request.method == "POST":
        form = HotelBookingForm(request.POST)
        if form.is_valid():
            booking_days = request.POST.get("booking_days")
            price = hotel.hotel_price
            booking_room = request.POST.get("booking_room")
            total_price = int(price) * int(booking_days) * int(booking_room)
            contact_no = request.POST.get("contact_no")
            address = request.POST.get("address")
            payment_method = request.POST.get("payment_method")            
            order = HotelBooking.objects.create(
                hotel=hotel,
                user=user,
                booking_days=booking_days,
                booking_room=booking_room,
                total_price=total_price,
                contact_no=contact_no,
                address=address,
                payment_method=payment_method,
            )

            if order.payment_method == "Cash on delivery":
                item = HotelCart.objects.get(uid=uid)
                item.delete()
                messages.add_message(
                    request, messages.SUCCESS, "Booking Successful, be ready with Cash"
                )
                return redirect("/users/mybook")
            elif order.payment_method == "Esewa":
                return redirect(
                    reverse("esewaform")
                    + "?o_uid="
                    + str(order.uid)
                    + "&c_uid="
                    + str(cart.uid)
                )
                
            else:
                messages.add_message(
                    request, messages.ERROR, "Kindly check the payment method"
                )
                return render(request, "publice/hotel_list.html", {"form": form})

        else:
            # Log form errors for debugging
            print(form.errors)
            messages.add_message(
                request, messages.ERROR, "Form is invalid. Please correct the errors."
            )

    context = {"form": HotelBookingForm}
    return render(request, "users/bookingform.html", context)

from django.views import View

import hmac  # cryptography algorithm
import hashlib  # encrypt data
import uuid  # to generate random string
import base64
class EsewaView(View):
    def get(self, request, *args, **kwargs):
        o_uid = request.GET.get("o_uid")
        c_uid = request.GET.get("c_uid")
        cart = HotelCart.objects.get(uid=c_uid)
        order = HotelBooking.objects.get(uid=o_uid)

        uuid_val = uuid.uuid4()

        def genSha256(key, message):
            key = key.encode("utf-8")
            message = message.encode("utf-8")

            hmac_sha256 = hmac.new(key, message, hashlib.sha256)

            digest = hmac_sha256.digest()

            signature = base64.b64encode(digest).decode("utf-8")
            return signature

        secret_key = "8gBm/:&EnhH.1/q"
        data_to_sign = f"total_amount={order.total_price}, transaction_uuid={uuid_val},product_code=EPAYTEST"

        result = genSha256(secret_key, data_to_sign)

        data = {
            "amount": order.hotel.hotel_price,
            "total_amount": order.total_price,
            "transaction_uuid": uuid_val,
            "product_code": "EPAYTEST",
            "signature": result,
        }
        context = {"order": order, "data": data, "cart": cart}
        return render(request, "users/esewa_payment.html", context)


import json


@login_required
def esewa_verify(request, b_uid, h_uid):
    if request.method == "GET":
        data = request.GET.get("data")
        decoded_data = base64.b64decode(data).decode("utf-8")
        map_data = json.loads(decoded_data)
        booking = HotelBooking.objects.get(id=b_uid)
        cart = HotelCart.objects.get(id=h_uid)

        if map_data.get("status") == "COMPLETE":
            booking.payment_status = True
            booking.save()
            cart.delete()
            messages.add_message(request, messages.SUCCESS, "Payment Successful")
            return redirect("/users/mybook")
        else:
            messages.add_message(request, messages.ERROR, "Failed to Make a Payment")
    return redirect("/users/mybook")


@login_required
def my_book(request):
    user = request.user
    items = HotelBooking.objects.filter(user=user)

    context = {"item": items}
    return render(request, "users/mybook.html", context)



@login_required
def my_book(request):
    user = request.user
    item = HotelCart.objects.filter(user=user)
    items = HotelBooking.objects.filter(user=user)

    context = {"items": items,"item": item}
    return render(request, "users/mybook.html", context)


@login_required
def profile(request):
    # user = User.objects.get(username=request.user)
    profile = UserProfile.objects.get(user=request.user)
    # cart = HotelCart.objects.all()
    context = {"profile": profile}
    return render(request, "users/profile.html", context)

# @login_required
# def update_profile(request):
#     if request.method == "POST":
#         form = ProfileUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.add_message(
#                 request, messages.SUCCESS, "Profile update Successfully"
#             )
#             return redirect("/users/profile")
#         else:
#             messages.add_message(request, messages.ERROR, "Failed to update profile")
#             return render(request, "users/updateprofile.html", {"form": form})

#     context = {"form": ProfileUpdateForm(instance=request.user)}

#     return render(request, "users/updateprofile.html", context)

@login_required
def update_profile(request):
    user = request.user
    try:
        # Fetch the user's profile
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # If no profile exists, handle the error (e.g., create a new one or show an error message)
        profile = UserProfile.objects.create(user=user)
        messages.warning(request, "No profile found, a new one has been created.")

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("/users/profile")  # Redirect to the profile page after successful update
        else:
            messages.error(request, "Failed to update profile. Please check the form for errors.")
    else:
        # Display the form pre-filled with the current user's profile
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, "users/updateprofile.html", {"form": form})


# @login_required
# def profile(request):
#     user = User.objects.get(username=request.user)
#     profile = Profile.objects.all()
#     context = {"profile": profile, "user":user}
#     return render(request, "users/profile.html", context)



# @login_required
# def update_profile(request):
#     if request.method == "POST":
#         form = ProfileUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.add_message(
#                 request, messages.SUCCESS, "Profile update Successfully"
#             )
#             return redirect("/users/profile")
#         else:
#             messages.add_message(request, messages.ERROR, "Failed to update profile")
#             return render(request, "users/updateprofile.html", {"form": form})

#     context = {"form": ProfileUpdateForm(instance=request.user)}

#     return render(request, "users/updateprofile.html", context)
