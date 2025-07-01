from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from .views import RegisterView, LoginView, LogoutView
from carpoint import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/signup/', views.signup_view, name='signup'),
    path('cars/create/', views.create_car, name='create_car'),
    path('cars/<int:car_id>/', views.car_details, name='car_details'),
    path('cars/', views.car_list_view, name='car_list'),
    path('parts/create/', views.create_part, name='create_part'),
    path('parts/<int:part_id>/', views.part_details, name='part_details'),
    path('parts/', views.part_list_view, name='part_list'),
    path('blogs/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('search-results/', views.search_results, name='search_results'),
    path('deals/checkout/user/<int:user_id>/car/<int:car_id>/', views.make_a_deal_view, name='make-a-deal'),
    path('deals/checkout/user/<int:user_id>/part/<int:part_id>/', views.make_a_part_deal_view, name='make-a-part-deal'),
    path('deals/create/<str:product_type>/<int:product_id>/', views.create_deal, name='create_deal'),
    path('offers/', views.offer_list, name='offer_list'),
    path('deals/', views.deal_list, name='deal_list'),
    path('deal/<int:deal_id>/accept/', views.accept_deal_ajax, name='accept_deal'),
    path('deal/<int:deal_id>/reject/', views.reject_deal_ajax, name='reject_deal'),
    path("update-profile/", views.update_user_profile, name="update_profile"),
    path('upload-profile-image/', views.upload_profile_image, name='upload_profile_image'),
    path('users/modify/<int:user_id>/', views.modify_user_profile_information_view, name='modify_profile_information'),
    path('register/', RegisterView.as_view(), name='register'),
    path('do-login/', LoginView.as_view(), name='do_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)