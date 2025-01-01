from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate , login
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import (Amenities, Hotel, HotelBooking)
from . models import *
from django.db.models import Q
from . forms import *
from django.contrib.auth.forms import UserCreationForm
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

# Create your views here.




def check_booking(start_date  , end_date ,uid , room_count):
    qs = HotelBooking.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        hotel__uid = uid
        )
    
    if len(qs) >= room_count:
        return False
    
    return True

def home(request):
    user = request.user.id
    item = HotelCart.objects.filter(user=user)
    hotels_objs = Hotel.objects.all()[:4]
    return render(request, "publice/home.html", {"item":item, 'hotels_objs':hotels_objs})

def hotel_list(request):
    user = request.user.id
    item = HotelCart.objects.filter(user=user)
    amenities_objs = Amenities.objects.all()
    hotels_objs = Hotel.objects.all()

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    print(amenities)
    if sort_by:
        if sort_by == 'ASC':
            hotels_objs = hotels_objs.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotels_objs = hotels_objs.order_by('-hotel_price')

    if search:
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains = search) |
            Q(description__icontains = search) )


    if len(amenities):
       hotels_objs = hotels_objs.filter(amenities__amenity_name__in = amenities).distinct()



    context = {'amenities_objs' : amenities_objs , 'hotels_objs' : hotels_objs , 'sort_by' : sort_by 
    , 'search' : search , 'amenities' : amenities, 'item' : item}
    return render(request , 'publice/hotel_list.html' ,context)



def hotel_detail(request,uid):
    user = request.user.id
    item = HotelCart.objects.filter(user=user)
    hotel_obj = Hotel.objects.get(uid = uid)

    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout= request.POST.get('checkout')
        hotel = Hotel.objects.get(uid = uid)
        if not check_booking(checkin ,checkout  , uid , hotel.room_count):
            messages.warning(request, 'Hotel is already booked in these dates ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        HotelBooking.objects.create(hotel=hotel , user = request.user , start_date=checkin
        , end_date = checkout , booking_type  = 'Pre Paid')
        
        messages.success(request, 'Your booking has been saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

        
    
    return render(request , 'publice/hotel_detail.html' ,{
        'hotels_obj' :hotel_obj, "item":item
    })

# def login_page(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user_obj = User.objects.filter(username = username)

#         if not user_obj.exists():
#             messages.warning(request, 'Account not found ')
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#         user_obj = authenticate(username = username , password = password)
#         if not user_obj:
#             messages.warning(request, 'Invalid password ')
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#         login(request , user_obj)
#         return redirect('/')

        
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     return render(request ,'login.html')


# def register_page(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user_obj = User.objects.filter(username = username)

#         if user_obj.exists():
#             messages.warning(request, 'Username already exists')
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#         user = User.objects.create(username = username)
#         user.set_password(password)
#         user.save()
#         return redirect('/')

#     return render(request , 'register.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "User register successfully."
            )
            return redirect("/login")
        else:
            messages.add_message(request, messages.ERROR, "Kindly check all the field.")
            return render(request, "users/register.html", {"form": form})

    context = {"form": RegisterForm}
    return render(request, "users/register.html", context)



def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            users = authenticate(
                request, username=data["username"], password=data["password"]
            )

            if users is not None:
                login(request, users)
                if users.is_staff:
                    return redirect("/admins")
                
                else:
                    return redirect("/")
                return redirect("/publice/publice")
            else:
                messages.add_message(
                    request, messages.ERROR, "Please provide correct credential"
                )
                return render(request, "users/login.html", {"form": form})
    # form = LoginForm
    # context={
    #     'form':form
    # }
    return render(request, "users/login.html", {"form": LoginForm})


def logout_user(request):
    logout(request)
    return redirect("/")


# def contact(request):
#     user = request.user.id
#     item = HotelCart.objects.filter(user=user)
#     form = ContactForm(request.POST)
#     if form.is_valid():
#         data = form.cleaned_data
#         messages.add_message(request, messages.SUCCESS, "sent massage successfully")
#         return redirect('publice/contactsend')
#     else:
#         messages.add_message(request, messages.ERROR, "Could you please check your massage")
#     return render(request, "publice/contact.html", {"item":item})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send email
            try:
                # Attempt to send email
                send_mail(
                    f'Contact Form Submission - {subject}',
                    f'Name: {name}\naddress: {address}\nEmail: {email}\nphone: {phone}\nMessage: {message}',
                    'shresthabikal44@gmail.com',
                    ['shresthabikal44@gmail.com'],
                    fail_silently=False,
                )
            except Exception as e:
                # Print detailed exception information
                print(f"Error sending email: {e}")
                # Optional: Log the error for further analysis
                # logger.error(f"Error sending email: {e}")

            return redirect('/contact.html')  # Redirect to a success page

    else:
        form = ContactForm()

    return render(request, 'publice/contact.html', {'form': form})

def contactsend(request):
    messages.add_message(request, messages.SUCCESS, "sent massage successfully")
    return redirect("/publice/contact")

def about(request):
    user = request.user.id
    item = HotelCart.objects.filter(user=user)
    return render(request, "publice/about.html", {"item":item})

def feature(request):
    user = request.user.id
    item = HotelCart.objects.filter(user=user)
    return render(request, "publice/feature.html", {"item":item})


def blog(request):
    user = request.user.id
    item = HotelCart.objects.filter(user=user)
    hotels_objs = Hotel.objects.all()[:8]
    return render(request, "publice/blog.html", {"item":item, "hotels_objs":hotels_objs})


# def generate_verification_code():
#     return str(random.randint(100000, 999999))

# def send_verification_email(email, code , username):
#     subject = "Welcome to Hotel Booking - Verify Your Email"
#     message = f"Dear {username} ,Greetings from Hotel Booking! We're delighted to have you on board as part of our community, where finding your ideal Hotel or room for rent is just a few clicks away.\n \n Once verified, you'll gain access to a wide range of rental options tailored to your preferences. Whether it's a cozy apartment or a spacious house, we've got you covered.\n \n Your Verification Code: {code}  \n \n Thank you for choosing Mero Niwas. We look forward to helping you find your perfect space! \n \n Warm regards, \n The Mero Niwas Team."
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, email_from, recipient_list)


# def show_registerBroker(request):
#     if request.method == 'POST':
#         uname = request.POST.get("username").strip()
#         contact_number = request.POST.get("contactnumber").strip()
#         email = request.POST.get("email").strip()
#         password = request.POST.get("password").strip()
#         confirm_password = request.POST.get("confirm-password").strip()
#         gender = request.POST.getlist("gender")
#         profile_picture = request.FILES.get('profile-picture')
#         Citizen_front = request.FILES.get('citizenship-front')
#         Citizen_back = request.FILES.get('citizenship-back')
#         accountType = "broker"

#         if not uname or not contact_number or not email or not password or not confirm_password:
#             return HttpResponse("Please fill in all fields. Some fields are empty or only contain spaces.")
        
#         if User.objects.filter(username=uname).exists():
#             return HttpResponse("Username already exists. Please choose a different username.")
        
#         if User.objects.filter(email=email).exists():
#             return HttpResponse("Email already exists. Please choose a different email.")

#         if UserProfile.objects.filter(contact_number=contact_number).exists():
#             return HttpResponse("Contact number already exists. Please choose a different contact number.")

#         if password != confirm_password:
#             return HttpResponse("Your password and confirm password must be the same.")

#         if profile_picture:
#             file_extension = profile_picture.name.split('.')[-1].lower()
#             if file_extension not in ["jpg", "jpeg", "png", "gif"]:
#                 return HttpResponse("Please upload only image files (jpg, jpeg, png, gif).")
#         if Citizen_front:
#             file_extension = Citizen_front.name.split('.')[-1].lower()
#             if file_extension not in ["jpg", "jpeg", "png", "gif"]:
#                 return HttpResponse("Please upload only image files (jpg, jpeg, png, gif).")
#         if Citizen_back:
#             file_extension = Citizen_back.name.split('.')[-1].lower()
#             if file_extension not in ["jpg", "jpeg", "png", "gif"]:
#                 return HttpResponse("Please upload only image files (jpg, jpeg, png, gif).")

#         # Generate verification code and send email
#         verification_code = generate_verification_code()
#         send_verification_email(email, verification_code, uname)

#         # Temporarily store the user data in session
#         request.session['registration_data'] = {
#             'username': uname,
#             'contact_number': contact_number,
#             'email': email,
#             'gender': gender,
#             'profile_picture': profile_picture.name,
#             'password':password,
#             'citizenship_front': Citizen_front.name,
#             'citizenship_back': Citizen_back.name,
#             'accountType': accountType,
#             'verification_code': verification_code,
#         }

#         # Redirect to verification page
#         return redirect('/verify_emailbroker')

#     return render(request, 'home/registerbroker.html')

# def verify_emailbroker(request):
#     if request.method == 'POST':
#         input_code = request.POST.get("verification_code").strip()
#         registration_data = request.session.get('registration_data')

#         if not registration_data:
#             return HttpResponse("Session expired. Please register again.")

#         if input_code == registration_data['verification_code']:
#             # Create the user account and save the data to the database
#             user = User.objects.create_user(
#                 registration_data['username'],
#                 registration_data['email'],
#                 registration_data['password']
#             )
#             user.save()

#             profile = UserProfile(
#                 user=user,
#                 contact_number=registration_data['contact_number'],
#                 email=registration_data['email'],
#                 gender=registration_data['gender'],
#                 profile_picture=registration_data['profile_picture'],
#                 Citizen_front=registration_data['citizenship_front'],
#                 Citizen_back=registration_data['citizenship_back'],
#                 accountType=registration_data['accountType']
#             )
#             profile.save()

#             # Clear the session data
#             del request.session['registration_data']

#             return redirect('/LoginSuccess')
#         else:
#             return HttpResponse("Invalid verification code.")

#     return render(request, 'home/verify_emailbroker.html')

# def show_registerRegular(request):
#     if request.method == 'POST':
#         uname = request.POST.get("username").strip()
#         contact_number = request.POST.get("contactnumber").strip()
#         email = request.POST.get("email").strip()
#         password = request.POST.get("password").strip()
#         confirm_password = request.POST.get("confirm-password").strip()
#         gender = request.POST.getlist("gender")
#         profile_picture = request.FILES.get('profile-picture')
#         accountType = "regular"

#         if not uname or not contact_number or not email or not password or not confirm_password:
#             return HttpResponse("Please fill in all fields. Some fields are empty or only contain spaces.")
        
#         if User.objects.filter(username=uname).exists():
#             return HttpResponse("Username already exists. Please choose a different username.")
        
#         if User.objects.filter(email=email).exists():
#             return HttpResponse("Email already exists. Please choose a different email.")

#         if UserProfile.objects.filter(contact_number=contact_number).exists():
#             return HttpResponse("Contact number already exists. Please choose a different contact number.")

#         if password != confirm_password:
#             return HttpResponse("Your password and confirm password must be the same.")

#         if profile_picture:
#             file_extension = profile_picture.name.split('.')[-1].lower()
#             if file_extension not in ["jpg", "jpeg", "png", "gif"]:
#                 return HttpResponse("Please upload only image files (jpg, jpeg, png, gif).")

#         # Generate verification code and send email
#         verification_code = generate_verification_code()
#         send_verification_email(email, verification_code, uname)

#         # Temporarily store the user data in session
#         request.session['registration_data'] = {
#             'username': uname,
#             'contact_number': contact_number,
#             'email': email,
#             'gender': gender,
#             'profile_picture': profile_picture.name if profile_picture else None,
#             'password':password,
#             'accountType': accountType,
#             'verification_code': verification_code,
#         }

#         # Redirect to verification page
#         return redirect('/verify_emailregular')
        

#     return render(request, 'home/registerregular.html')

# def verify_emailregular(request):
#     if request.method == 'POST':
#         input_code = request.POST.get("verification_code").strip()
#         registration_data = request.session.get('registration_data')

#         if not registration_data:
#             return HttpResponse("Session expired. Please register again.")

#         if input_code == registration_data['verification_code']:
#             # Create the user account and save the data to the database
#             user = User.objects.create_user(
#                 registration_data['username'],
#                 registration_data['email'],
#                 registration_data['password']
#             )
#             user.save()

#             profile = UserProfile(
#                 user=user,
#                 contact_number=registration_data['contact_number'],
#                 email=registration_data['email'],
#                 gender=registration_data['gender'],
#                 profile_picture=registration_data['profile_picture'],
#                 accountType=registration_data['accountType']
#             )
#             profile.save()

#             # Clear the session data
#             del request.session['registration_data']

#             return redirect('/LoginSuccess')
#         else:
#             return HttpResponse("Invalid verification code.")

#     return render(request, 'home/verify_emailregular.html')