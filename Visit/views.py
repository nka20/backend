from site import USER_BASE
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import *
from .models import *
from .serializers import *
from django.contrib.auth.models import User
### create user
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
#########
# change password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from .serializers import ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from .serializers import ChangePasswordSerializer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.urls import reverse
# 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
# from django_user_agents.utils import get_user_agent
from rest_framework.views import APIView
from datetime import datetime, time
from .models import PageView
from .serializers import PageViewSerializer
from rest_framework import generics
from rest_framework import status

###########################################################################
class TokenPairView(TokenObtainPairView):
	serializer_class = TokenPairSerializer
    
def get_user_agent(request):
    user_agent = request.META['HTTP_USER_AGENT']
    return user_agent

# create user 
class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    ###############################
#  change password #######################################
def my_view(request):
    # Cette vue suppose que l'utilisateur est authentifié, mais si ce n'est pas le cas,
    # cela pourrait entraîner l'erreur mentionnée.
    return HttpResponse("Hello, authenticated user!")

class MyPutView(View):
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        # Your view logic for handling PUT requests
        return HttpResponse("PUT request processed successfully")

# @login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, User)
            return redirect(reverse('company:Dashboard'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Supprimer le jeton d'authentification existant, s'il existe
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()

        # Créer un nouveau jeton d'authentification
        token, created = Token.objects.get_or_create(user=user)

        # Retourner le nouveau jeton
        return Response({'token': token.key}, status=status.HTTP_200_OK)

class ListAllTokensView(APIView):
    def get(self, request, *args, **kwargs):
        # Récupérer tous les objets Token
        all_tokens = Token.objects.all()

        # Traiter les objets Token selon vos besoins
        token_data = [{'user_id': token.user.id, 'key': token.key} for token in all_tokens]

        # Retourner les données sous forme de réponse JSON
        return Response({'tokens': token_data}, status=status.HTTP_200_OK)
# ###########################################################
class Photo_hotelsViewSet(viewsets.ModelViewSet):
    queryset = Photo_hotel.objects.all()
    serializer_class = Photo_hotelsSerializer
    filterset_fields = ['hotel']
    search_fields = ['hotel']   

class hotelsViewset(viewsets.ModelViewSet):
    queryset = hotels.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = hotelsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = hotels.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return hotels.objects.all()
    filterset_fields = ['id']
    search_fields = ['name']
    
    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__icontains', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = hotels.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return hotels.objects.all()

    @action(methods=["GET"], detail=True, url_path=r'update-visit-count', url_name=r'update-visit-count', serializer_class=hotelsSerializer)
    def updateVisitCount(self, request, pk):
        instance: hotels = hotels.objects.get(id=pk)
        instance.visit_count += 1

        instance.save()
        serializer = hotelsSerializer(instance, many=False)

        return Response(serializer.data, 200)

    @action(methods=["GET"], detail=False, url_name="max", url_path="max")
    def getMax(self, request):
        qs = hotels.objects.all()
        items = []

        for i in qs:
            if i.visit_count > 0:
                items.append(i)

        serializer = hotelsSerializer(items, many=True).data
        return Response(serializer, 200)

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        return super().list(request, *args, **kwargs)

##########################################################################
class reservationViewset(viewsets.ModelViewSet):
    queryset = reservation.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = reservationSerializer
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['service']
    # search_fields = ['service']

class Reservations_of_servicesViewset(viewsets.ModelViewSet):
    queryset = Reservations_of_services.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = Reservations_of_servicesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['services_of_hotels']
    search_fields = ['reservations']

class Reservations_of_restaurantsViewset(viewsets.ModelViewSet):
    queryset = Reservations_of_restaurants.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = Reservations_of_restaurantsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['restaurants_bars']
    search_fields = ['reservations']
########################################################################
class Photo_serviceViewSet(viewsets.ModelViewSet):
    queryset = Photo_service.objects.all()
    serializer_class = Photo_serviceSerializer

class Service_of_hotelsViewset(viewsets.ModelViewSet):
    queryset = Services_of_hotels.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = Services_of_hotelsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['services']
    search_fields = ['hotel']

class Service_of_restaurantsViewset(viewsets.ModelViewSet):
    queryset = Services_of_restaurants_bars.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = Services_of_restaurantsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['restaurants_bars']
    search_fields = ['services']

class serviceViewset(viewsets.ModelViewSet):
    queryset = service.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = serviceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

#############################################################################
class Photo_guideViewSet(viewsets.ModelViewSet):
    queryset = Photo_guide.objects.all()
    serializer_class = Photo_guideSerializer
    filterset_fields = ['guide']
    search_fields = ['guide'] 

class GuideViewset(viewsets.ModelViewSet):
    queryset = Guide.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = GuideSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = Guide.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return Guide.objects.all()
    
class Guides_of_hotelsViewset(viewsets.ModelViewSet):
    queryset = Guides_of_hotels.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = Guides_of_hotelsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['hotel']
    search_fields = ['hotel']

class Photo_guideViewSet(viewsets.ModelViewSet):
    queryset = Photo_guide.objects.all()
    serializer_class = Photo_guideSerializer
    filterset_fields = ['guide']
    search_fields = ['guide']  


class GuideViewset(viewsets.ModelViewSet):
    queryset = Guide.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = GuideSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']


    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = Guide.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return Guide.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)

###########################################################################
class Photo_restaurant_barsViewSet(viewsets.ModelViewSet):
    queryset = Photo_restaurant_bars.objects.all()
    serializer_class = Photo_restaurant_barsSerializer
    filterset_fields = ['restaurant_bars']
    search_fields = ['restaurant_bars']

class restaurant_barsViewset(viewsets.ModelViewSet):
    queryset = restaurant_bars.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = restaurant_barsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = restaurant_bars.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return restaurant_bars.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
####################################################################
class Photo_foodViewSet(viewsets.ModelViewSet):
    queryset = Photo_food.objects.all()
    serializer_class = Photo_foodSerializer
    filterset_fields = ['food']
    search_fields = ['food']   

class foodViewset(viewsets.ModelViewSet):
    queryset = food.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = foodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['prix']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        prix_min = self.request.query_params.get('prix__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if prix_min is not None and prix_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = food.objects.filter(prix__gte=int(prix_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return food.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
    
# class FoodMostViewedPages(APIView):
#     def get(self, request):
#         most_viewed_pages = foodViewset.objects.order_by(
#             '-view_count')[:10]  # Récupérer les 10 pages les plus vues
#         serializer = foodSerializer(most_viewed_pages, many=True)
#         return Response(serializer.data)
    
#     def get(self, request, *args, **kwargs):
#         # Get data from the request (e.g., page and url)
#         page = request.query_params.get('page', '')
#         url = request.query_params.get('url', '')

#         # Try to get an existing food
#         pageView, created = PageView.objects.get_or_create(page=page, url=url)
#         pageView.save()

#         # Serialize the food data
#         serializer = PageViewSerializer(food)

#         # Return the serialized data
#         return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

#############################################################################
class Photo_nightclubsViewSet(viewsets.ModelViewSet):
    queryset = Photo_nightclubs.objects.all()
    serializer_class = Photo_nightclubsSerializer
    filterset_fields = ['nightclubs']
    search_fields = ['nightclubs'] 

class nightclubsViewset(viewsets.ModelViewSet):
    queryset = nightclubs.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = nightclubsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = nightclubs.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return nightclubs.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
########################################################################

class Photo_sitestouristiquesViewSet(viewsets.ModelViewSet):
    queryset = Photo_sitestouristiques.objects.all()
    serializer_class = Photo_sitestouristiquesSerializer
    filterset_fields = ['sitestouristiques']
    search_fields = ['sitestouristiques']   

class sitestouristiquesViewset(viewsets.ModelViewSet):
    queryset = sitestouristiques.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = sitestouristiquesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = sitestouristiques.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return sitestouristiques.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
########################################################################
class Photo_eventViewSet(viewsets.ModelViewSet):
    queryset = Photo_event.objects.all()
    serializer_class = Photo_eventSerializer
    filterset_fields = ['event']
    search_fields = ['event']   

class eventViewset(viewsets.ModelViewSet):
    queryset = event.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = eventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['open_time']
    search_fields = ['name']

    @action(methods=["GET"], detail=False, url_path=r'get-event-date', url_name=r'get-event-date', serializer_class=eventSerializer)
    def getEventDate(self, request):
        first_hour = datetime.combine(datetime.today(), time(hour=0))
        last_hour = datetime.combine(
            datetime.today(), time(hour=23, minute=59, second=59))
        events = event.objects.filter(
            open_time__gte=first_hour, close_time__lte=last_hour
        )
        serializer = eventSerializer(events, many=True)

        return Response(serializer.data, 200)

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
###########################################################################
class Photo_lieux_de_loisirsViewSet(viewsets.ModelViewSet):
    queryset = Photo_lieux_de_loisirs.objects.all()
    serializer_class = Photo_lieux_de_loisirsSerializer
    filterset_fields = ['lieux_de_loisirs']
    search_fields = ['lieux_de_loisirs']   

class lieux_de_loisirsViewset(viewsets.ModelViewSet):
    queryset = lieux_de_loisirs.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = lieux_de_loisirsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = lieux_de_loisirs.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return lieux_de_loisirs.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
#################################################################
class Photo_provinceViewSet(viewsets.ModelViewSet):
    queryset = Photo_province.objects.all()
    serializer_class = Photo_provinceSerializer
    filterset_fields = ['province']
    search_fields = ['province']  
    

class provinceViewset(viewsets.ModelViewSet):
    queryset = province.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = provinceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']


    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = province.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return province.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
###########################################################################
class Photo_quartiersViewSet(viewsets.ModelViewSet):
    queryset = Photo_quartiers.objects.all()
    serializer_class = Photo_quartiersSerializer
    filterset_fields = ['quartiers']
    search_fields = ['quartiers']  

class quartiersViewset(viewsets.ModelViewSet):
    queryset = quartiers.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = quartiersSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = quartiers.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return quartiers.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)

##############################################################################
class Photo_churchesViewSet(viewsets.ModelViewSet):
    queryset = Photo_churches.objects.all()
    serializer_class = Photo_churchesSerializer
    filterset_fields = ['churches']
    search_fields = ['churches']   

class churchesViewset(viewsets.ModelViewSet):
    queryset = churches.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = churchesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__icontains', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = churches.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return churches.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        # return Response({"ip": str(ip), "agent": (user_agent)}, 200)
        return super().list(request, *args, **kwargs)
#######################################################################
class Photo_marketViewSet(viewsets.ModelViewSet):
    queryset = Photo_market.objects.all()
    serializer_class = Photo_marketSerializer
    filterset_fields = ['market']
    search_fields = ['market']  

class marketViewset(viewsets.ModelViewSet):
    queryset = market.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = marketSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = market.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return market.objects.all()

    

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
##########################################################################
class Photo_hospitalsViewSet(viewsets.ModelViewSet):
    queryset = Photo_hospitals.objects.all()
    serializer_class = Photo_hospitalsSerializer
    filterset_fields = ['hospitals']
    search_fields = ['hospitals']  

class hospitalsViewset(viewsets.ModelViewSet):
    queryset = hospitals.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = hospitalsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = hospitals.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return hospitals.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
#########################################################################
class Photo_transportViewSet(viewsets.ModelViewSet):
    queryset = Photo_transport.objects.all()
    serializer_class = Photo_transportSerializer
    filterset_fields = ['transport']
    search_fields = ['transport']  

class transportViewset(viewsets.ModelViewSet):
    queryset = transport.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = transportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = transport.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return transport.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)

#################################################################
class Photo_conferenceViewSet(viewsets.ModelViewSet):
    queryset = Photo_conference.objects.all()
    serializer_class = Photo_conferenceSerializer
    filterset_fields = ['conference']
    search_fields = ['conference']  

class conferenceViewset(viewsets.ModelViewSet):
    queryset = conference.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = conferenceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name_court']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = conference.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return conference.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
###################################################################
class Photo_cultureViewSet(viewsets.ModelViewSet):
    queryset = Photo_culture.objects.all()
    serializer_class = Photo_cultureSerializer
    filterset_fields = ['culture'] 
    search_fields = ['culture'] 

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    filterset_fields = ['name'] 
    search_fields = ['name']  

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        photo_instance, created = photo.objects.get_or_create(name=data['name'])

        if created:
            photo_instance.image = data['image']
        else:
            photo_instance.image = data['image']

        photo_instance.save()


        return Response(201)

class cultureViewset(viewsets.ModelViewSet):
    queryset = culture.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = cultureSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = culture.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return culture.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
########################################################################
class Photo_artViewSet(viewsets.ModelViewSet):
    queryset = Photo_art.objects.all()
    serializer_class = Photo_artSerializer
    filterset_fields = ['art']
    search_fields = ['art'] 

# class tendanceViewset(viewsets.ModelViewSet):
#     queryset = Tendance.objects.all()
#     serializer_class = TendanceSerializer
#     filterset_fields = ['page']
#     search_fields = ['page'] 

#     def create(self, request):
#         data = request.data

#         tendance_instance, created = Tendance.objects.get_or_create(id=data.get('id'))

#         tendance_instance.page = data.get('page', '')
#         tendance_instance.image = data.get('image', '')
#         tendance_instance.lien = data.get('lien', '')


#         tendance_instance.save()

#         return Response(status=status.HTTP_201_CREATED)
class tendanceViewset (viewsets.ModelViewSet):
    queryset = Tendance.objects.all()
    serializer_class = TendanceSerializer
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    filterset_fields = ['lien']
    search_fields = ['identification'] 

    def create(self, request):
        data = request.data

        tendance_instance, created = Tendance.objects.get_or_create(origine=data['origine'],identification=data['identification'])

        if created:
            tendance_instance.page = data['page']
            tendance_instance.origine = data['origine']
            tendance_instance.image = data['image']
            tendance_instance.identification = data['identification']
            tendance_instance.lien = data['lien']
        else:
            tendance_instance.page = data['page']
            tendance_instance.origine = data['origine']
            tendance_instance.lien = data['lien']
            tendance_instance.identification = data['identification']
            tendance_instance.image = data['image']

        tendance_instance.save()
        return Response(201)

class informationViewset (viewsets.ModelViewSet):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    filterset_fields = ['nom']
    search_fields = ['nom'] 

class artViewset(viewsets.ModelViewSet):
    queryset = art.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly,
    authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = artSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

    def get_queryset(self):
        # Récupérer la valeur du paramètre 'prix' dans l'URL
        stars_min = self.request.query_params.get('stars__gte', None)

        # Assurez-vous que la valeur est présente et est un nombre valide
        if stars_min is not None and stars_min.isdigit():
            # Filtrer les hôtels avec un prix supérieur ou égal à la valeur spécifiée
            queryset = art.objects.filter(stars__gte=int(stars_min))
            return queryset

        # Si la valeur n'est pas présente ou n'est pas valide, retourner un queryset complet
        return art.objects.all()

    def list(self, request, *args, **kwargs):
        user_agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        print(ip)

        return super().list(request, *args, **kwargs)
######################################################################



########################################################################
# class vues(APIView):
#     def get(self, request):
#         count = request.session.get('count', 0)
#         request.session['count'] = count + 1

class MostViewedPages(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = PageView.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = PageViewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['page']
    search_fields = ['page']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        page,created = PageView.objects.get_or_create(page=data['page'])
        if(created):
            page.url=data['url']
            page.count =data['count']
            page.image = data['image']
        else:
            page.image= data['image']
            page.count+=data['count']
        
        page.save()

        return Response(201)


#####################################################################
# class MostViewedPages(APIView):   
#     def get(self, request):
#         most_viewed_pages = PageView.objects.all().order_by('-count')[:10]  # Récupérer les 10 pages les plus vues
#         serializer = PageViewSerializer(most_viewed_pages, many=True)
#         return Response(serializer.data)

# @action(methods=["GET"], detail=True, url_path=r'update-visit-count', url_name=r'update-visit-count', serializer_class=hotelsSerializer)
# def updateVisitCount(self, request, pk):
#         instance: hotels = hotels.objects.get(id=pk)
#         instance.visit_count += 1

#         instance.save()
#         serializer = hotelsSerializer(instance, many=False)

#         return Response(serializer.data, 200)

# class PageViewList(generics.ListCreateAPIView):
#     queryset = PageView.objects.all()
#     serializer_class = PageViewSerializer
################################les pages les plus vues###################################
class view_guideViewset(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_guide.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_guideSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_guide_instance, created = view_guide.objects.get_or_create(identification=data['identification'])

        if created:
            view_guide_instance.page = data['page']
            view_guide_instance.image = data['image']
            view_guide_instance.identification = data['identification']
            view_guide_instance.count = data['count']
        else:
            view_guide_instance.page = data['page']
            view_guide_instance.identification = data['identification']
            view_guide_instance.image = data['image']
            view_guide_instance.count += data['count']

        view_guide_instance.save()


        return Response(201)
    
class view_artViewset(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_art.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_guideSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_art_instance, created = view_art.objects.get_or_create(identification=data['identification'])

        if created:
            view_art_instance.page = data['page']
            view_art_instance.image = data['image']
            view_art_instance.identification = data['identification']
            view_art_instance.count = data['count']
        else:
            view_art_instance.page = data['page']
            view_art_instance.identification = data['identification']
            view_art_instance.image = data['image']
            view_art_instance.count += data['count']

        view_art_instance.save()
        return Response(201)
    
class view_hotelViewset(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_hotel.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_hotelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_hotel_instance, created = view_hotel.objects.get_or_create(identification=data['identification'])

        if created:
            view_hotel_instance.page = data['page']
            view_hotel_instance.image = data['image']
            view_hotel_instance.identification = data['identification']
            view_hotel_instance.count = data['count']
        else:
            view_hotel_instance.page = data['page']
            view_hotel_instance.identification = data['identification']
            view_hotel_instance.image = data['image']
            view_hotel_instance.count += data['count']

        view_hotel_instance.save()
        return Response(201)
class views_restaurant_barsViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_restaurant_bars.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_restaurant_barsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_restaurant_bars_instance, created = view_restaurant_bars.objects.get_or_create(identification=data['identification'])

        if created:
            view_restaurant_bars_instance.page = data['page']
            view_restaurant_bars_instance.image = data['image']
            view_restaurant_bars_instance.identification = data['identification']
            view_restaurant_bars_instance.count = data['count']
        else:
            view_restaurant_bars_instance.page = data['page']
            view_restaurant_bars_instance.identification = data['identification']
            view_restaurant_bars_instance.image = data['image']
            view_restaurant_bars_instance.count += data['count']

        view_restaurant_bars_instance.save()


        return Response(201)
    
class view_foodViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_food.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_foodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_food_instance, created = view_food.objects.get_or_create(identification=data['identification'])

        if created:
            view_food_instance.page = data['page']
            view_food_instance.image = data['image']
            view_food_instance.identification = data['identification']
            view_food_instance.count = data['count']
        else:
            view_food_instance.page = data['page']
            view_food_instance.identification = data['identification']
            view_food_instance.image = data['image']
            view_food_instance.count += data['count']

        view_food_instance.save()


        return Response(201)
class view_conferenceViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_conference.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_conferenceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_conference_instance, created = view_conference.objects.get_or_create(identification=data['identification'])

        if created:
            view_conference_instance.page = data['page']
            view_conference_instance.image = data['image']
            view_conference_instance.identification = data['identification']
            view_conference_instance.count = data['count']
        else:
            view_conference_instance.page = data['page']
            view_conference_instance.identification = data['identification']
            view_conference_instance.image = data['image']
            view_conference_instance.count += data['count']

        view_conference_instance.save()


        return Response(201)
    
    

class view_eventViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_event.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_eventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_event_instance, created = view_event.objects.get_or_create(identification=data['identification'])

        if created:
            view_event_instance.page = data['page']
            view_event_instance.image = data['image']
            view_event_instance.identification = data['identification']
            view_event_instance.count = data['count']
        else:
            view_event_instance.page = data['page']
            view_event_instance.identification = data['identification']
            view_event_instance.image = data['image']
            view_event_instance.count += data['count']

        view_event_instance.save()


        return Response(201)
class view_churchesViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_churches.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_churchesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_churches_instance, created = view_churches.objects.get_or_create(identification=data['identification'])

        if created:
            view_churches_instance.page = data['page']
            view_churches_instance.image = data['image']
            view_churches_instance.identification = data['identification']
            view_churches_instance.count = data['count']
        else:
            view_churches_instance.page = data['page']
            view_churches_instance.identification = data['identification']
            view_churches_instance.image = data['image']
            view_churches_instance.count += data['count']

        view_churches_instance.save()


        return Response(201)
class view_sitestouristiquesViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_sitestouristiques.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_sitestouristiquesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_sitestouristiques_instance, created = view_sitestouristiques.objects.get_or_create(identification=data['identification'])

        if created:
            view_sitestouristiques_instance.page = data['page']
            view_sitestouristiques_instance.image = data['image']
            view_sitestouristiques_instance.identification = data['identification']
            view_sitestouristiques_instance.count = data['count']
        else:
            view_sitestouristiques_instance.page = data['page']
            view_sitestouristiques_instance.identification = data['identification']
            view_sitestouristiques_instance.image = data['image']
            view_sitestouristiques_instance.count += data['count']

        view_sitestouristiques_instance.save()


        return Response(201)
class view_marketViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_market.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_marketSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_market_instance, created = view_market.objects.get_or_create(identification=data['identification'])

        if created:
            view_market_instance.page = data['page']
            view_market_instance.image = data['image']
            view_market_instance.identification = data['identification']
            view_market_instance.count = data['count']
        else:
            view_market_instance.page = data['page']
            view_market_instance.identification = data['identification']
            view_market_instance.image = data['image']
            view_market_instance.count += data['count']

        view_market_instance.save()


        return Response(201)
        
    
class view_lieux_de_loisirsViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_lieux_de_loisirs.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_lieux_de_loisirsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_lieux_de_loisirs_instance, created = view_lieux_de_loisirs.objects.get_or_create(identification=data['identification'])

        if created:
            view_lieux_de_loisirs_instance.page = data['page']
            view_lieux_de_loisirs_instance.image = data['image']
            view_lieux_de_loisirs_instance.identification = data['identification']
            view_lieux_de_loisirs_instance.count = data['count']
        else:
            view_lieux_de_loisirs_instance.page = data['page']
            view_lieux_de_loisirs_instance.identification = data['identification']
            view_lieux_de_loisirs_instance.image = data['image']
            view_lieux_de_loisirs_instance.count += data['count']

        view_lieux_de_loisirs_instance.save()
        return Response(201)
     
class view_provinceViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_province.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_provinceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_province_instance, created = view_province.objects.get_or_create(identification=data['identification'])

        if created:
            view_province_instance.page = data['page']
            view_province_instance.image = data['image']
            view_province_instance.identification = data['identification']
            view_province_instance.count = data['count']
        else:
            view_province_instance.page = data['page']
            view_province_instance.identification = data['identification']
            view_province_instance.image = data['image']
            view_province_instance.count += data['count']

        view_province_instance.save()
        return Response(201) 
class view_quartiersViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_quartiers.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_quartiersSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_quartiers_instance, created = view_quartiers.objects.get_or_create(identification=data['identification'])

        if created:
            view_quartiers_instance.page = data['page']
            view_quartiers_instance.image = data['image']
            view_quartiers_instance.identification = data['identification']
            view_quartiers_instance.count = data['count']
        else:
            view_quartiers_instance.page = data['page']
            view_quartiers_instance.identification = data['identification']
            view_quartiers_instance.image = data['image']
            view_quartiers_instance.count += data['count']

        view_quartiers_instance.save()
        return Response(201) 
class view_hospitalViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_hospital.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_hospitalSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_hospital_instance, created = view_hospital.objects.get_or_create(identification=data['identification'])

        if created:
            view_hospital_instance.page = data['page']
            view_hospital_instance.image = data['image']
            view_hospital_instance.identification = data['identification']
            view_hospital_instance.count = data['count']
        else:
            view_hospital_instance.page = data['page']
            view_hospital_instance.identification = data['identification']
            view_hospital_instance.image = data['image']
            view_hospital_instance.count += data['count']

        view_hospital_instance.save()
        return Response(201) 
class view_nightclubsViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_nightclubs.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_nightclubsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_nightclubs_instance, created = view_nightclubs.objects.get_or_create(identification=data['identification'])

        if created:
            view_nightclubs_instance.page = data['page']
            view_nightclubs_instance.image = data['image']
            view_nightclubs_instance.identification = data['identification']
            view_nightclubs_instance.count = data['count']
        else:
            view_nightclubs_instance.page = data['page']
            view_nightclubs_instance.identification = data['identification']
            view_nightclubs_instance.image = data['image']
            view_nightclubs_instance.count += data['count']

            view_nightclubs_instance.save()
            return Response(201) 
class view_cultureViewSet(viewsets.ModelViewSet):
    # queryset = PageView.objects.all().order_by('-count')[:10]
    queryset = view_culture.objects.all().order_by('-count')
    # permission_classes = IsAuthenticatedOrReadOnly,
    # authentication_classes= JWTAuthentication, SessionAuthentication
    serializer_class = view_cultureSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['identification']
    search_fields = ['identification']

    def create(self, request):
        data = request.data

        # Créer un nouvel objet PageView avec les autres champs
        view_culture_instance, created = view_culture.objects.get_or_create(identification=data['identification'])

        if created:
            view_culture_instance.page = data['page']
            view_culture_instance.image = data['image']
            view_culture_instance.identification = data['identification']
            view_culture_instance.count = data['count']
        else:
            view_culture_instance.page = data['page']
            view_culture_instance.identification = data['identification']
            view_culture_instance.image = data['image']
            view_culture_instance.count += data['count']

        view_culture_instance.save()
        return Response(201) 
    
