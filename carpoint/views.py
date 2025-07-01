from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .decorators import seller_required
from .models import BlogPost, Car, Part, UserProfile, Deal
from .forms import CarForm, PartForm
from .models import CarImage
from .models.part import PartImage
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseBadRequest



@login_required
def index(request):
    blogs = BlogPost.objects.order_by('-publish_date')[:3]
    cars = Car.objects.order_by('-created_at')[:6]
    parts = Part.objects.order_by('-rating')[:3]
    return render(request, 'index.html', {
        'blogs': blogs,
        'cars': cars,
        'parts': parts,
    })
@login_required
def create_deal(request, product_type, product_id):
    if request.method == 'POST':
        proposal = request.POST.get('proposal')
        if not proposal:
            return HttpResponseBadRequest("Proposal is required.")

        try:
            proposal = float(proposal)
        except ValueError:
            return HttpResponseBadRequest("Invalid proposal value.")

        if product_type == 'car':
            product = get_object_or_404(Car, id=product_id)
        elif product_type == 'part':
            product = get_object_or_404(Part, id=product_id)
        else:
            return HttpResponseBadRequest("Invalid product type.")

        seller = product.seller
        customer = request.user

        content_type = ContentType.objects.get_for_model(product)

        deal = Deal.objects.create(
            customer=customer,
            seller=seller,
            proposal=proposal,
            content_type=content_type,
            object_id=product.id
        )

        return render(request, 'deal/deal_success.html', {'deal': deal})

    return HttpResponseBadRequest("Invalid request method.")



@login_required
def offer_list(request):
    seller = request.user
    deals = Deal.objects.filter(seller=seller).order_by('-created_at')
    return render(request, 'offers/offer_list.html', {'deals': deals})
@login_required
def deal_list(request):
    customer = request.user
    deals = Deal.objects.filter(customer=customer).order_by('-created_at')
    return render(request, 'deal/deal_list.html', {'deals': deals})
@login_required
def accept_deal_ajax(request, deal_id):
    if request.method == 'POST':
        deal = get_object_or_404(Deal, id=deal_id, seller=request.user)
        deal.status = 'accepted'
        deal.save()
        return JsonResponse({'success': True, 'new_status': deal.status})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def reject_deal_ajax(request, deal_id):
    if request.method == 'POST':
        deal = get_object_or_404(Deal, id=deal_id, seller=request.user)
        deal.status = 'rejected'
        deal.save()
        return JsonResponse({'success': True, 'new_status': deal.status})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def make_a_deal_view(request, user_id, car_id):
    car = get_object_or_404(Car, pk=car_id)
    seller = get_object_or_404(UserProfile, user__id=user_id)
    return render(request, 'deal/deal.html', {'seller': seller,"car": car})
@login_required
def make_a_part_deal_view(request, user_id, part_id):
    part = get_object_or_404(Part, pk=part_id)
    seller = get_object_or_404(UserProfile, user__id=user_id)
    return render(request, 'deal/part_deal.html', {'seller': seller,"part": part})
@login_required
def modify_user_profile_information_view(request, user_id):
    userprofile = get_object_or_404(UserProfile, user__id=user_id)
    return render(request, 'user_profile/modify_profile_information.html', {'userprofile': userprofile})
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'auth/login.html')


@csrf_exempt
@login_required
def update_user_profile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        field = data.get("field")
        value = data.get("value")
        userprofile = request.user.userprofile

        if field == "name":
            parts = value.split()
            request.user.first_name = parts[0]
            request.user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
            request.user.save()
        elif field == "phone":
            userprofile.phone = value
            userprofile.save()
        elif field == "address":
            userprofile.address = value
            userprofile.save()
        elif field == "email":
            request.user.email = value
            request.user.save()
        else:
            return JsonResponse({"error": "Invalid field"}, status=400)

        return JsonResponse({"status": "success"})

    return JsonResponse({"error": "Invalid request"}, status=400)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'auth/inscrit.html')
@seller_required
def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            car.seller = request.user
            car.save()
            gallery_images = request.FILES.getlist('gallery_images')
            for image in gallery_images:
                CarImage.objects.create(car=car, image=image)
            return redirect('car_details', car_id=car.id)
    else:
        form = CarForm()
    return render(request, 'cars/create_car.html', {'form': form})
def car_details(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    gallery = car.gallery_images.all()
    return render(request, 'cars/car_details.html', {
        'car': car,
        'gallery': gallery
    })
@login_required
@require_POST
def upload_profile_image(request):
    user_profile = request.user.userprofile
    image_file = request.FILES.get('image')
    if image_file:
        user_profile.image.save(image_file.name, image_file)
        user_profile.save()
        return JsonResponse({'status': 'success', 'image_url': user_profile.image.url})
    return JsonResponse({'status': 'error'}, status=400)
def car_list_view(request):
    car_list = Car.objects.all().order_by('-created_at')
    paginator = Paginator(car_list, 6)

    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)

    return render(request, 'cars/cars.html', {'cars': cars})
@seller_required
def create_part(request):
    if request.method == 'POST':
        form = PartForm(request.POST, request.FILES)
        if form.is_valid():
            part = form.save()
            part.seller = request.user
            part.save()
            gallery_images = request.FILES.getlist('gallery_images')
            for image in gallery_images:
                PartImage.objects.create(part=part, image=image)
            return redirect('part_details', part_id=part.id)
    else:
        form = PartForm()
    return render(request, 'parts/create_part.html', {'form': form})
def part_details(request, part_id):
    part = get_object_or_404(Part, pk=part_id)
    gallery = part.gallery_images.all()
    return render(request, 'parts/part_details.html', {
        'part': part,
        'gallery': gallery
    })

def part_list_view(request):
    part_list = Part.objects.all().order_by('-rating')
    paginator = Paginator(part_list, 6)

    page_number = request.GET.get('page')
    parts = paginator.get_page(page_number)

    return render(request, 'parts/parts.html', {'parts': parts})
def blog_details(request, blog_id):
    blog = get_object_or_404(BlogPost, pk=blog_id)
    return render(request, 'blog/blog-details.html', {
        'blog': blog,
    })

def search_results(request):
    query = request.GET.get('q', '').strip()

    cars_list = []
    parts_list = []

    if query:
        cars_list = Car.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(color__icontains=query) |
            Q(fuel_type__icontains=query) |
            Q(transmission__icontains=query)
        ).order_by('-created_at')

        parts_list = Part.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-id')

    cars_paginator = Paginator(cars_list, 8)
    cars_page_number = request.GET.get('cars_page')
    cars_page_obj = cars_paginator.get_page(cars_page_number)

    parts_paginator = Paginator(parts_list, 8)
    parts_page_number = request.GET.get('parts_page')
    parts_page_obj = parts_paginator.get_page(parts_page_number)

    context = {
        'query': query,
        'cars': cars_page_obj,
        'parts': parts_page_obj,
    }
    return render(request, 'search/search_results.html', context)

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'auth/inscrit.html')

    def post(self, request):
        serializer = RegisterSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'auth/login.html', {'error': 'Email not found'})
            user = authenticate(username=user_obj.username, password=password)
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                response = redirect('index')
                response.set_cookie(
                    key='jwt',
                    value=str(refresh.access_token),
                    httponly=True,
                    samesite='Lax',
                )
                return response
            return render(request, 'auth/inscrit.html', {'errors': serializer.errors})
        return render(request, 'auth/inscrit.html', {'errors': serializer.errors})

class LoginView(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'auth/login.html', {'error': 'Email not found'})

        user = authenticate(username=user_obj.username, password=password)

        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            response = redirect('index')
            response.set_cookie(
                key='jwt',
                value=str(refresh.access_token),
                httponly=True,
                samesite='Lax',
            )
            return response

        return render(request, 'auth/login.html', {'error': 'Invalid credentials'})

    def get(self, request):
        return render(request, 'auth/login.html')
class LogoutView(View):
    def get(self, request):
        response = redirect('login')
        response.delete_cookie('jwt')
        response.delete_cookie('csrftoken')
        response.delete_cookie('sessionid')
        return response
