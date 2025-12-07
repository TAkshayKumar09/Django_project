from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import users
from .models import fooditems
import cloudinary.uploader
import bcrypt

# Create your views here.
@csrf_exempt
def register(req):
    if req.method=="POST":
        name=req.POST.get('name')
        email=req.POST.get('email')
        mobile=req.POST.get('mobile')
        password=req.POST.get('password')

        hashed=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(rounds=12)).decode('utf-8')
    user=users.objects.create(name=name, email=email, mobile=mobile, password=hashed)
    return HttpResponse('User Created Successfully')

@csrf_exempt
def login(req):
    if req.method == "POST":
        email=req.POST.get('email')
        password=req.POST.get('password')

        try:
            check=users.objects.get(email=email) 
            stored_hash=check.password

            is_same=bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
            if is_same:
                return HttpResponse("Login Successfully")
            else:
                return HttpResponse('Invalid Credentials')
        
        except users.DoesNotExist:
            return HttpResponse("Invalid Credentials")
    return HttpResponse("Invalid Request Method", status=405)



@csrf_exempt
def update_user(req, email):
    if req.method == "POST":
        user=users.objects.get(email=email)

        try:
            user.password=req.POST.get("password", user.password)

            # new_password=req.POST.get("password")
            # if new_password:
            #     user.password=new_password
            
            user.save()
            return HttpResponse("Password Changed")
        except users.DoesNotExist:
            return HttpResponse("Invalid Email")


@csrf_exempt
def delete_user(req):
    if req.method == "POST":
        email=req.POST.get("email")
        password=req.POST.get("password")

        try:
            user=users.objects.get(email=email, password=password)
            user.delete()

            return HttpResponse("User Deleted")
        except users.DoesNotExist:
            return HttpResponse("User Not Found")





@csrf_exempt
def get_menu(req):
    data=fooditems.objects.all().values()

    list_data= list(data)
    return JsonResponse(list_data, safe=False)


@csrf_exempt
def createmenu(req):
    name=req.POST.get("name")
    description=req.POST.get("description")
    price=req.POST.get("price")
    category=req.POST.get("category")

    image=req.FILES.get("image")
    img_url=cloudinary.uploader.upload(image)
    print(img_url)
    new=fooditems.objects.create(name=name, description=description, price=price, image=img_url['secure_url'], category=category)
    
    return HttpResponse ("Created......")


@csrf_exempt
def update_menu(req,name):
    if req.method == "POST":
        try:
            item=fooditems.objects.get(name=name)

            item.name=req.POST.get("name", item.name)
            item.description=req.POST.get("description", item.description)
            item.price=req.POST.get("price", item.price)
            item.category=req.POST.get("category", item.category)

            new_image=req.FILES.get("image")
            if new_image:
                img_url=cloudinary.uploader.upload(new_image)
                item.image=img_url['secure_url']

            item.save()
            return HttpResponse('Updated')
        except fooditems.DoesNotExist:
            return HttpResponse("Item Not Found")



@csrf_exempt
def delete_item(req):
    if req.method == "POST":
        name=req.POST.get("name")

        try:
            menu=fooditems.objects.get(name=name)
            menu.delete()

            return HttpResponse("Deleted Item")
        except fooditems.DoesNotExist:
            return HttpResponse("Item Not Found")