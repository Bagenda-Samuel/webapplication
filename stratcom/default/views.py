import imp
from django.shortcuts import render, redirect
from django.http import HttpResponse, request, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from . models import UserProfile, InternshipApplications, Gallery
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

# Create your views here.
def homepage(request, *args, **kwargs):
    if request.method == "POST":
        fname = request.POST['fname']
        sname = request.POST['sname']
        uname = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                user = User.objects.create(
                    first_name = fname,
                    last_name = sname,
                    username = uname,
                    email = email,
                )
                user.set_password(password)
                user.save()
                if request.FILES['pp']:
                    pp = request.FILES['pp']
                    user_id = user.id
                    UserProfile.objects.create(
                        owner = User.objects.get(id=user_id),
                        pp = pp
                    )
                messages.info(request, "User Has been created successfully")
            except:
                messages.info(request, "User Already Exists!")
        else:
            print("passwords do not match")
            messages.info("The passwords do not match")
        print(request.POST)
    context = {
    }
    response = render(request, "index.html",context)
    return response

def login_page(request, *args, **kwargs):
    if request.method == "POST":
        uname = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=uname, password = password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return redirect("/dashboard/")
        else:
            messages.info(request, "Invalid Credentials!")
    context = {
    }
    if request.user.is_authenticated:
        return redirect("/dashboard/")
    response = render(request, "login.html",context)
    return response

def logout_page(request, *args, **kwargs):
    logout(request)
    return redirect("/")


def contact_page(request, *args, **kwargs):
    context = {
    }
    response = render(request, "contact.html",context)
    return response

def gallery_page(request, *args, **kwargs):
    if request.method == "POST":
        id = request.POST['id']
        figcaption = request.POST['caption']
        toUpdate = Gallery.objects.get(id=id)
        toUpdate.figcaption = figcaption
        if request.FILES:
            pic = request.FILES['gallery']
            toUpdate.pic.delete()
            toUpdate.pic = pic
        toUpdate.save()
        return HttpResponse(json.dumps({"message":"update successfull"}))
    gallery_items = Gallery.objects.all().order_by("-id")
    paged = Paginator(gallery_items, 6)
    page = request.GET.get("page")
    delete = request.GET.get("delete")
    update = request.GET.get("update")
    if update:
        to_update_item = Gallery.objects.get(id=update)
        context = {
            "gallery":to_update_item
        }
        return render(request, "update.html", context)
    if delete:
        to_delete_item = Gallery.objects.get(id=delete)
        if to_delete_item.pic:
            to_delete_item.pic.delete()
        to_delete_item.delete()
    if page:
        gallery_items = paged.get_page(page)
        request.session['page'] = page
    elif 'page' in request.session.keys():
        gallery_items = paged.get_page(request.session['page'])
    else:
        gallery_items = paged.get_page(1)
    context = {
        "gallery_items":gallery_items
    }
    response = render(request, "gallery.html",context)
    return response

def about_page(request, *args, **kwargs):
    context = {
    }
    response = render(request, "about.html",context)
    return response

@login_required(login_url="/login/")  
def dashboard_page(request, *args, **kwargs):
    if request.method == "POST":
        gender = request.POST['gender']
        dob = request.POST['date']
        university = request.POST['university']
        letter = request.FILES['letter']
        areas = request.POST['areas']
        count_of_application = InternshipApplications.objects.filter(owner=request.user).count()
        if count_of_application == 0:
            InternshipApplications.objects.create(
                owner = request.user,
                gender = gender,
                dob = dob,
                application_letter = letter,
                areas_of_interest = areas,
                university = university
            )
            messages.info(request, "Your Application Has Been Recieved!")
        else:
            messages.info(request, "You can only apply once!")
    status = request.GET.get("view")
    message = None
    if status:
        try:
            my_status = InternshipApplications.objects.get(owner=request.user).qualified
            if my_status == True:
                message = "Congratulations, report with immediate efect for training"
            else:
                message = "Application is still under review"
        except:
            message = "You Have not yet Applied!"

    user_profile = UserProfile.objects.get(owner=request.user)
    context = {
        "user_profile":user_profile,
        "status_application":message
    }
    response = render(request, "dashboard.html",context)
    return response