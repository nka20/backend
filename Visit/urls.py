"""
URL configuration for local_visit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from .views import UserListAPIView
from .views import UserDeleteAPIView
from .views import *
# suspend an user 

from .views import UserDetailView

# password change
from django.contrib import admin
from django.urls import path
##### create user
from .views import UserRegistrationView
##########
from .views import MyPutView
# 
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MostViewedPages
from .views import view_guideViewset

router = routers.DefaultRouter()

router.register("photos_hotels", Photo_hotelsViewSet)
router.register("hotels", hotelsViewset)
router.register("photos_service", Photo_serviceViewSet)
router.register("service", serviceViewset )
router.register("Services_of_hotels", Service_of_hotelsViewset )
router.register("Services_of_restaurants", Service_of_restaurantsViewset )
router.register("photos_guide", Photo_guideViewSet)
router.register("guides_of_hotels", Guides_of_hotelsViewset)
router.register("Guide", GuideViewset )
router.register("reservation", reservationViewset )
router.register("reservations_of_hotels", Reservations_of_servicesViewset)
router.register("reservations_of_restaurants", Reservations_of_restaurantsViewset)
router.register("photos_restaurant", Photo_restaurant_barsViewSet )
router.register("restaurant_bars", restaurant_barsViewset )
router.register("photos_food", Photo_foodViewSet )
router.register("food", foodViewset )
router.register("photos_nightclubs", Photo_nightclubsViewSet)
router.register("nightclubs", nightclubsViewset )
router.register("photos_sitestouristiques", Photo_sitestouristiquesViewSet)
router.register("sitestouristiques", sitestouristiquesViewset )
router.register("photos_event", Photo_eventViewSet)
router.register("event", eventViewset )
router.register("photos_lieux_de_loisirs", Photo_lieux_de_loisirsViewSet)
router.register("lieux_de_loisirs", lieux_de_loisirsViewset )
router.register("photos_province", Photo_provinceViewSet )
router.register("province", provinceViewset )
router.register("photos_quartiers", Photo_quartiersViewSet )
router.register("quartiers", quartiersViewset )
router.register("photos_churches", Photo_churchesViewSet )
router.register("churches", churchesViewset )
router.register("photos_market", Photo_marketViewSet )
router.register("market", marketViewset )
router.register("photos_hospitals", Photo_hospitalsViewSet )
router.register("hospitals", hospitalsViewset )
router.register("tendance", tendanceViewset )
router.register("information", informationViewset )
router.register("photos_transport", Photo_transportViewSet )
router.register("transport", transportViewset )
router.register("photos_culture", Photo_cultureViewSet)
router.register("culture", cultureViewset )
router.register("photo", PhotoViewSet )
router.register("photos_art", Photo_artViewSet )
router.register("art", artViewset )
router.register("photos_conference", Photo_conferenceViewSet )
router.register("conference", conferenceViewset )
router.register("viewedpage", MostViewedPages )
router.register("view_guide", view_guideViewset)
router.register("view_art", view_artViewset)
router.register("view_hotel", view_hotelViewset)
router.register("view_restaurant_bars", views_restaurant_barsViewSet)
router.register("view_food", view_foodViewSet)
router.register("view_food", view_conferenceViewSet)
router.register("view_event", view_eventViewSet)
router.register("view_churches", view_churchesViewSet)
router.register("view_sitestouristiques", view_sitestouristiquesViewSet)
router.register("view_market", view_marketViewSet)
router.register("view_lieux_de_loisirs", view_lieux_de_loisirsViewSet)
router.register("view_province", view_provinceViewSet)
router.register("view_quartiers", view_quartiersViewSet)
router.register("view_hospital", view_hospitalViewSet)
router.register("view_nightclubs", view_nightclubsViewSet)
router.register("view_culture", view_cultureViewSet)


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/', UserListAPIView.as_view(), name='user'),
    path('user-suspend/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    #   path('change-authorization/<int:pk>/', ChangeAuthorizationView.as_view(), name='change-authorization'),
    path('user/<int:pk>/', UserDeleteAPIView.as_view(), name='user-delete'),
    # ... other paths ...
    path('', include(router.urls)),
    # change password
    path('my-view/', my_view, name='my_view'),
    #  path('admin/', admin.site.urls),
     path('change-username/', ChangeUsernameView.as_view(), name='change_username'),
    # path('Visit/', include('visit.urls')),  # Remplacez "myapp" par le nom de votre application
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('your/endpoint/', MyPutView.as_view(), name='my_put_view'),
    # ###########
    path('login/',TokenPairView.as_view()),
    path('refresh/',TokenRefreshView.as_view()),
    path('api-auth/',include('rest_framework.urls')),
    # path('most-viewed-pages/', MostViewedPages.as_view(), name='most_viewed_pages'),
]
