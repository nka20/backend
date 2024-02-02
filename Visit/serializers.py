<<<<<<< HEAD
from rest_framework import serializers
from .models import *
# from django.contrib.auth import password_validation
# create an user
from django.contrib.auth.models import User
####
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from .models import PageView

class TokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(TokenPairSerializer, self).validate(attrs)
        access_token = self.get_token(self.user)
        data['expiredAt'] = access_token['exp']
        data['username'] = self.user.username
        data['id'] = self.user.id
        data['is_superuser'] = self.user.is_superuser
        data['is_active'] = self.user.is_active
        data['is_authorized'] = getattr(self.user, 'is_authorized', True)

        return data

class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_active']

    def get_token(self, obj):
        # Utilize the TokenObtainPairSerializer module to generate a token
        refresh = TokenObtainPairSerializer.get_token(obj)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data

    def create(self, validated_data):
        # Extract is_authorized from validated_data
        is_authorized = validated_data.pop('is_authorized', False)

        # Create the user with the remaining data
        user = User.objects.create_user(**validated_data)

        # Set is_authorized for the created user
        user.is_authorized = is_authorized
        user.save()

        # Generate the token
        token_serializer = TokenObtainPairSerializer()
        token_data = token_serializer.validate({'username': validated_data['username'], 'password': validated_data['password']})

        # Add the token to the user data
        user.token = token_data['access']

        # Include is_authorized in the serialized output
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        # You can add more fields to update as needed

        # Save the changes to the user instance
        instance.save()
        return instance

        #
# change password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                ('Your old password was entered incorrectly or your username is already used. Please enter it again.')
            )
        return value  

    def create(self, validated_data):
        user = self.context['request'].user

        # Mettre à jour le mot de passe avec le nouveau
        user.set_password(validated_data['new_password1'])
        user.save()

        return user
        # ################


  # change username

class ChangeUsernameSerializer(serializers.Serializer):
    Username = serializers.CharField(max_length=128, write_only=True, required=True)
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                ('Your old password was entered incorrectly or your username is already used. Please enter it again.')
            )
        return value  

    def create(self, validated_data):
        user = self.context['request'].user

        # Mettre à jour le username avec le nouveau
        user.username = validated_data['Username']
        user.save()

        return user
        ##############      
class Photo_hotelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_hotel
        fields = "__all__"    
            
class hotelsSerializer(serializers.ModelSerializer):
    photo_hotels= serializers.SerializerMethodField()

    def get_photo_hotels(self, hotel):
        qs = Photo_hotel.objects.all().filter(hotel=hotel)
        serializer = Photo_hotelsSerializer(instance=qs , many = True)
        return serializer.data
    # def to_representation(self, instance):
    #      data = super().to_representation(instance)
    #      data["service_name"] = instance.service.name
    #      data["service_price"] = instance.service.price
         
        # return data
     
     ##Kubaz si ngaha noshiramwo ivya reservation comme nayo ifise foreign_key muri service
    class Meta:
        model = hotels
        fields = "__all__"
######################################################    

#####################################################################        
class Photo_restaurant_barsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_restaurant_bars
        fields = "__all__"
class restaurant_barsSerializer(serializers.ModelSerializer):
    photo_restaurant_bars= serializers.SerializerMethodField()
    def get_photo_restaurant_bars(self, restaurant_bars):
        qs = Photo_restaurant_bars.objects.all().filter(restaurant_bars=restaurant_bars)
        serializer = Photo_restaurant_barsSerializer(instance=qs , many = True)
        return serializer.data
    def to_representation(self, instance):
         data = super().to_representation(instance)
         #data["service_name"] = instance.service.name
         #data["service_price"] = instance.service.price
         return data
    class Meta:
        model = restaurant_bars
        fields = "__all__"

############################################################
class Photo_foodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_food
        fields = "__all__"
class foodSerializer(serializers.ModelSerializer):
    photo_food= serializers.SerializerMethodField()
    def get_photo_food(self, food):
        qs = Photo_food.objects.all().filter(food=food)
        serializer = Photo_foodSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = food
        fields = "__all__"
###############################################################
class Photo_guideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_guide
        fields = "__all__"
class GuideSerializer(serializers.ModelSerializer):
    photo_guide= serializers.SerializerMethodField()
    def get_photo_guide(self, guide):
        qs = Photo_guide.objects.all().filter(guide=guide)
        serializer = Photo_guideSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = Guide
        fields = "__all__"
    
class Guides_of_hotelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guides_of_hotels
        fields = "__all__"
class TendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tendance
        fields = "__all__"
class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = "__all__"

###############################################################
class Photo_nightclubsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_nightclubs
        fields = "__all__"

class nightclubsSerializer(serializers.ModelSerializer):
    photo_nightclubs= serializers.SerializerMethodField()
    def get_photo_nightclubs(self, nightclubs):
        qs = Photo_nightclubs.objects.all().filter(nightclubs=nightclubs)
        serializer = Photo_nightclubsSerializer(instance=qs , many = True)
        return serializer.data
    # def to_representation(self, instance):
    #      data = super().to_representation(instance)
    #      data["service_name"] = instance.service.name
    #     #  data["service_price"] = instance.service.price
    #      return data
    class Meta:
        model = nightclubs
        fields = "__all__"
###############################################################
class Photo_sitestouristiquesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_sitestouristiques
        fields = "__all__"       
class sitestouristiquesSerializer(serializers.ModelSerializer):
    photo_sitestouristiques= serializers.SerializerMethodField()
    def get_photo_sitestouristiques(self, sitestouristiques):
        qs = Photo_sitestouristiques.objects.all().filter(sitestouristiques=sitestouristiques)
        serializer = Photo_sitestouristiquesSerializer(instance=qs , many = True)
        return serializer.data

    def to_representation(self,object):  
        representation=super().to_representation(object)
          # representation["guide"]=GuideSerializer(object.guide,many=False).data
        return representation

    class Meta:
        model = sitestouristiques
        fields = "__all__"
###############################################################
class Photo_eventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_event
        fields = "__all__"       
class eventSerializer(serializers.ModelSerializer):
    photo_event= serializers.SerializerMethodField()
    def get_photo_event(self, event):
        qs = Photo_event.objects.all().filter(event=event)
        serializer = Photo_eventSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = event
        fields = "__all__"
############################################################
class Photo_lieux_de_loisirsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_lieux_de_loisirs
        fields = "__all__"       
class lieux_de_loisirsSerializer(serializers.ModelSerializer):
    photo_lieux_de_loisirs= serializers.SerializerMethodField()
    def get_photo_lieux_de_loisirs(self, lieux_de_loisirs):
        qs =  Photo_lieux_de_loisirs.objects.all().filter(lieux_de_loisirs=lieux_de_loisirs)
        serializer = Photo_lieux_de_loisirsSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = lieux_de_loisirs
        fields = "__all__"
###########################################################
class Photo_provinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_province
        fields = "__all__"
class provinceSerializer(serializers.ModelSerializer):
    photo_province= serializers.SerializerMethodField()
    def get_photo_province(self, province):
        qs = Photo_province.objects.all().filter(province=province)
        serializer = Photo_provinceSerializer(instance=qs , many = True)
        return serializer.data

    def to_representation(self,object):
        representation=super().to_representation(object)
          # representation["guide"]=GuideSerializer(object.guide,many=False).data
        return representation
    class Meta:
        model = province
        fields = "__all__"
########################################################
class Photo_quartiersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_quartiers
        fields = "__all__"
class quartiersSerializer(serializers.ModelSerializer):
    photo_quartiers= serializers.SerializerMethodField()
    def get_photo_quartiers(self,quartiers):
        qs = Photo_quartiers.objects.all().filter(quartiers=quartiers)
        serializer = Photo_quartiersSerializer(instance=qs , many = True)
        return serializer.data

    def to_representation(self,object):
        representation=super().to_representation(object)
          # representation["guide"]=GuideSerializer(object.guide,many=False).data
        return representation
    class Meta:
        model = quartiers
        fields = "__all__"
    
########################################################
class Photo_churchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_churches
        fields = "__all__"
class churchesSerializer(serializers.ModelSerializer):
       photo_churches= serializers.SerializerMethodField()
       def get_photo_churches(self, churches):
        qs = Photo_churches.objects.all().filter(churches=churches)
        serializer = Photo_churchesSerializer(instance=qs , many = True)
        return serializer.data
       class Meta:
        model = churches
        fields = "__all__"
#############################################################
class Photo_marketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_market
        fields = "__all__"
class marketSerializer(serializers.ModelSerializer):
    photo_market= serializers.SerializerMethodField()
    def get_photo_market(self, market):
        qs = Photo_market.objects.all().filter(market=market)
        serializer = Photo_marketSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = market
        fields = "__all__"

#############################################################
class Photo_hospitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_hospitals
        fields = "__all__"
class hospitalsSerializer(serializers.ModelSerializer):
    photo_hospitals= serializers.SerializerMethodField()
    def get_photo_hospitals(self, hospitals):
        qs = Photo_hospitals.objects.all().filter(hospitals=hospitals)
        serializer = Photo_hospitalsSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = hospitals
        fields = "__all__"
#################################################################

class Photo_transportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_transport
        fields = "__all__"
class transportSerializer(serializers.ModelSerializer):
    photo_transport= serializers.SerializerMethodField()
    def get_photo_transport(self,transport):
        qs = Photo_transport.objects.all().filter(transport=transport)
        serializer = Photo_transportSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = transport
        fields = "__all__"
###################################################################
class Photo_conferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_conference
        fields = "__all__"
class conferenceSerializer(serializers.ModelSerializer):
    photo_conference= serializers.SerializerMethodField()
    def get_photo_conference(self, conference):
        qs = Photo_conference.objects.all().filter(conference=conference)
        serializer = Photo_conferenceSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
         model = conference
         fields = "__all__" 
###########################################################################
class Photo_cultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_culture
        fields = "__all__"
class cultureSerializer(serializers.ModelSerializer):
    photo_culture= serializers.SerializerMethodField()
    def get_photo_culture(self, culture):
        qs = Photo_culture.objects.all().filter(culture=culture)
        serializer = Photo_cultureSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
         model = culture
         fields = "__all__"

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = photo
        fields = "__all__"

###########################################################
class Photo_artSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_art
        fields = "__all__"
class artSerializer(serializers.ModelSerializer):
    photo_art= serializers.SerializerMethodField()
    def get_photo_art(self,art):
        qs = Photo_art.objects.all().filter(art=art)
        serializer = Photo_artSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
         model = art
         fields = "__all__"
###################################les pages les plus vues##################################
class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        fields = "__all__"
        
class view_guideSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_guide
        fields = "__all__"

class view_artSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_art
        fields = "__all__"

class view_hotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_hotel
        fields = "__all__"
class view_transportSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_transport
        fields = "__all__"

class view_restaurant_barsSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_restaurant_bars
        fields = "__all__"

class view_foodSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_food
        fields = "__all__"

class view_conferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_conference
        fields = "__all__"
        
class view_eventSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_event
        fields = "__all__"
class view_churchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_churches
        fields = "__all__"

class view_sitestouristiquesSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_sitestouristiques
        fields = "__all__"
                
class view_marketSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_market
        fields = "__all__"
class view_lieux_de_loisirsSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_lieux_de_loisirs
        fields = "__all__"

class view_provinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_province
        fields = "__all__"

class view_quartiersSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_province
        fields = "__all__"
        
class view_hospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_hospital
        fields = "__all__"
class view_nightclubsSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_nightclubs
        fields = "__all__"
class view_cultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_culture
        fields = "__all__"
=======
from rest_framework import serializers
from .models import *
# from django.contrib.auth import password_validation
# create an user
from django.contrib.auth.models import User
####
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from .models import PageView

class TokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(TokenPairSerializer, self).validate(attrs)
        access_token = self.get_token(self.user)
        data['expiredAt'] = access_token['exp']
        data['username'] = self.user.username
        data['id'] = self.user.id
        data['is_superuser'] = self.user.is_superuser
        data['is_active'] = self.user.is_active
        data['is_authorized'] = getattr(self.user, 'is_authorized', True)

        return data

class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_active']

    def get_token(self, obj):
        # Utilize the TokenObtainPairSerializer module to generate a token
        refresh = TokenObtainPairSerializer.get_token(obj)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data

    def create(self, validated_data):
        # Extract is_authorized from validated_data
        is_authorized = validated_data.pop('is_authorized', False)

        # Create the user with the remaining data
        user = User.objects.create_user(**validated_data)

        # Set is_authorized for the created user
        user.is_authorized = is_authorized
        user.save()

        # Generate the token
        token_serializer = TokenObtainPairSerializer()
        token_data = token_serializer.validate({'username': validated_data['username'], 'password': validated_data['password']})

        # Add the token to the user data
        user.token = token_data['access']

        # Include is_authorized in the serialized output
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        # You can add more fields to update as needed

        # Save the changes to the user instance
        instance.save()
        return instance

        #
# change password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                ('Your old password was entered incorrectly or your username is already used. Please enter it again.')
            )
        return value  

    def create(self, validated_data):
        user = self.context['request'].user

        # Mettre à jour le mot de passe avec le nouveau
        user.set_password(validated_data['new_password1'])
        user.save()

        return user
        # ################


  # change username

class ChangeUsernameSerializer(serializers.Serializer):
    Username = serializers.CharField(max_length=128, write_only=True, required=True)
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                ('Your old password was entered incorrectly or your username is already used. Please enter it again.')
            )
        return value  

    def create(self, validated_data):
        user = self.context['request'].user

        # Mettre à jour le username avec le nouveau
        user.username = validated_data['Username']
        user.save()

        return user
        ##############      
class Photo_hotelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_hotel
        fields = "__all__"    
            
class hotelsSerializer(serializers.ModelSerializer):
    photo_hotels= serializers.SerializerMethodField()

    def get_photo_hotels(self, hotel):
        qs = Photo_hotel.objects.all().filter(hotel=hotel)
        serializer = Photo_hotelsSerializer(instance=qs , many = True)
        return serializer.data
    # def to_representation(self, instance):
    #      data = super().to_representation(instance)
    #      data["service_name"] = instance.service.name
    #      data["service_price"] = instance.service.price
         
        # return data
     
     ##Kubaz si ngaha noshiramwo ivya reservation comme nayo ifise foreign_key muri service
    class Meta:
        model = hotels
        fields = "__all__"
######################################################    

#####################################################################        
class Photo_restaurant_barsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_restaurant_bars
        fields = "__all__"
class restaurant_barsSerializer(serializers.ModelSerializer):
    photo_restaurant_bars= serializers.SerializerMethodField()
    def get_photo_restaurant_bars(self, restaurant_bars):
        qs = Photo_restaurant_bars.objects.all().filter(restaurant_bars=restaurant_bars)
        serializer = Photo_restaurant_barsSerializer(instance=qs , many = True)
        return serializer.data
    def to_representation(self, instance):
         data = super().to_representation(instance)
         #data["service_name"] = instance.service.name
         #data["service_price"] = instance.service.price
         return data
    class Meta:
        model = restaurant_bars
        fields = "__all__"

############################################################
class Photo_foodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_food
        fields = "__all__"
class foodSerializer(serializers.ModelSerializer):
    photo_food= serializers.SerializerMethodField()
    def get_photo_food(self, food):
        qs = Photo_food.objects.all().filter(food=food)
        serializer = Photo_foodSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = food
        fields = "__all__"
###############################################################
class Photo_guideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_guide
        fields = "__all__"
class GuideSerializer(serializers.ModelSerializer):
    photo_guide= serializers.SerializerMethodField()
    def get_photo_guide(self, guide):
        qs = Photo_guide.objects.all().filter(guide=guide)
        serializer = Photo_guideSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = Guide
        fields = "__all__"
    
class Guides_of_hotelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guides_of_hotels
        fields = "__all__"
class TendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tendance
        fields = "__all__"
class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = "__all__"

###############################################################
class Photo_nightclubsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_nightclubs
        fields = "__all__"

class nightclubsSerializer(serializers.ModelSerializer):
    photo_nightclubs= serializers.SerializerMethodField()
    def get_photo_nightclubs(self, nightclubs):
        qs = Photo_nightclubs.objects.all().filter(nightclubs=nightclubs)
        serializer = Photo_nightclubsSerializer(instance=qs , many = True)
        return serializer.data
    # def to_representation(self, instance):
    #      data = super().to_representation(instance)
    #      data["service_name"] = instance.service.name
    #     #  data["service_price"] = instance.service.price
    #      return data
    class Meta:
        model = nightclubs
        fields = "__all__"
###############################################################
class Photo_sitestouristiquesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_sitestouristiques
        fields = "__all__"       
class sitestouristiquesSerializer(serializers.ModelSerializer):
    photo_sitestouristiques= serializers.SerializerMethodField()
    def get_photo_sitestouristiques(self, sitestouristiques):
        qs = Photo_sitestouristiques.objects.all().filter(sitestouristiques=sitestouristiques)
        serializer = Photo_sitestouristiquesSerializer(instance=qs , many = True)
        return serializer.data

    def to_representation(self,object):  
        representation=super().to_representation(object)
          # representation["guide"]=GuideSerializer(object.guide,many=False).data
        return representation

    class Meta:
        model = sitestouristiques
        fields = "__all__"
###############################################################
class Photo_eventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_event
        fields = "__all__"       
class eventSerializer(serializers.ModelSerializer):
    photo_event= serializers.SerializerMethodField()
    def get_photo_event(self, event):
        qs = Photo_event.objects.all().filter(event=event)
        serializer = Photo_eventSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = event
        fields = "__all__"
############################################################
class Photo_lieux_de_loisirsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_lieux_de_loisirs
        fields = "__all__"       
class lieux_de_loisirsSerializer(serializers.ModelSerializer):
    photo_lieux_de_loisirs= serializers.SerializerMethodField()
    def get_photo_lieux_de_loisirs(self, lieux_de_loisirs):
        qs =  Photo_lieux_de_loisirs.objects.all().filter(lieux_de_loisirs=lieux_de_loisirs)
        serializer = Photo_lieux_de_loisirsSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = lieux_de_loisirs
        fields = "__all__"
###########################################################
class Photo_provinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_province
        fields = "__all__"
class provinceSerializer(serializers.ModelSerializer):
    photo_province= serializers.SerializerMethodField()
    def get_photo_province(self, province):
        qs = Photo_province.objects.all().filter(province=province)
        serializer = Photo_provinceSerializer(instance=qs , many = True)
        return serializer.data

    def to_representation(self,object):
        representation=super().to_representation(object)
          # representation["guide"]=GuideSerializer(object.guide,many=False).data
        return representation
    class Meta:
        model = province
        fields = "__all__"
########################################################
class Photo_quartiersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_quartiers
        fields = "__all__"
class quartiersSerializer(serializers.ModelSerializer):
    photo_quartiers= serializers.SerializerMethodField()
    def get_photo_quartiers(self,quartiers):
        qs = Photo_quartiers.objects.all().filter(quartiers=quartiers)
        serializer = Photo_quartiersSerializer(instance=qs , many = True)
        return serializer.data

    def to_representation(self,object):
        representation=super().to_representation(object)
          # representation["guide"]=GuideSerializer(object.guide,many=False).data
        return representation
    class Meta:
        model = quartiers
        fields = "__all__"
    
########################################################
class Photo_churchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_churches
        fields = "__all__"
class churchesSerializer(serializers.ModelSerializer):
       photo_churches= serializers.SerializerMethodField()
       def get_photo_churches(self, churches):
        qs = Photo_churches.objects.all().filter(churches=churches)
        serializer = Photo_churchesSerializer(instance=qs , many = True)
        return serializer.data
       class Meta:
        model = churches
        fields = "__all__"
#############################################################
class Photo_marketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_market
        fields = "__all__"
class marketSerializer(serializers.ModelSerializer):
    photo_market= serializers.SerializerMethodField()
    def get_photo_market(self, market):
        qs = Photo_market.objects.all().filter(market=market)
        serializer = Photo_marketSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = market
        fields = "__all__"

#############################################################
class Photo_hospitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_hospitals
        fields = "__all__"
class hospitalsSerializer(serializers.ModelSerializer):
    photo_hospitals= serializers.SerializerMethodField()
    def get_photo_hospitals(self, hospitals):
        qs = Photo_hospitals.objects.all().filter(hospitals=hospitals)
        serializer = Photo_hospitalsSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = hospitals
        fields = "__all__"
#################################################################

class Photo_transportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_transport
        fields = "__all__"
class transportSerializer(serializers.ModelSerializer):
    photo_transport= serializers.SerializerMethodField()
    def get_photo_transport(self,transport):
        qs = Photo_transport.objects.all().filter(transport=transport)
        serializer = Photo_transportSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
        model = transport
        fields = "__all__"
###################################################################
class Photo_conferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_conference
        fields = "__all__"
class conferenceSerializer(serializers.ModelSerializer):
    photo_conference= serializers.SerializerMethodField()
    def get_photo_conference(self, conference):
        qs = Photo_conference.objects.all().filter(conference=conference)
        serializer = Photo_conferenceSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
         model = conference
         fields = "__all__" 
###########################################################################
class Photo_cultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_culture
        fields = "__all__"
class cultureSerializer(serializers.ModelSerializer):
    photo_culture= serializers.SerializerMethodField()
    def get_photo_culture(self, culture):
        qs = Photo_culture.objects.all().filter(culture=culture)
        serializer = Photo_cultureSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
         model = culture
         fields = "__all__"

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = photo
        fields = "__all__"

###########################################################
class Photo_artSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_art
        fields = "__all__"
class artSerializer(serializers.ModelSerializer):
    photo_art= serializers.SerializerMethodField()
    def get_photo_art(self,art):
        qs = Photo_art.objects.all().filter(art=art)
        serializer = Photo_artSerializer(instance=qs , many = True)
        return serializer.data
    class Meta:
         model = art
         fields = "__all__"
###################################les pages les plus vues##################################
class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        fields = "__all__"
        
class view_guideSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_guide
        fields = "__all__"

class view_artSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_art
        fields = "__all__"

class view_hotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_hotel
        fields = "__all__"
class view_transportSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_transport
        fields = "__all__"

class view_restaurant_barsSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_restaurant_bars
        fields = "__all__"

class view_foodSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_food
        fields = "__all__"

class view_conferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_conference
        fields = "__all__"
        
class view_eventSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_event
        fields = "__all__"
class view_churchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_churches
        fields = "__all__"

class view_sitestouristiquesSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_sitestouristiques
        fields = "__all__"
                
class view_marketSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_market
        fields = "__all__"
class view_lieux_de_loisirsSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_lieux_de_loisirs
        fields = "__all__"

class view_provinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_province
        fields = "__all__"

class view_quartiersSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_province
        fields = "__all__"
        
class view_hospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_hospital
        fields = "__all__"
class view_nightclubsSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_nightclubs
        fields = "__all__"
class view_cultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = view_culture
        fields = "__all__"
>>>>>>> 7f9daa9cb5a76769bcf6559e422025052719d683
