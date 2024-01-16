from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
# from multiupload.fields import MultiImageField
# Create your models here.

class User(User):
    is_authorized = models.BooleanField(default=False)


class Photo_hotel(models.Model):
    #amafoto ya ma hotels azoja muri photos_hotels ,aho ha upload to, aho naho ha related_name hazojamwo ibindi
    image = models.ImageField(upload_to='photos_hotels')
    hotel = models.ForeignKey('hotels', related_name='photo_hotels', on_delete=models.CASCADE)
    # restaurant = models.ForeignKey('restaurant', related_name='visit_restaurant', on_delete=models.CASCADE)
    # food = models.ForeignKey('food', related_name='visit_food', on_delete=models.CASCADE)
    # bar = models.ForeignKey('bar', related_name='visit_bar', on_delete=models.CASCADE) 
    # sites_touristiques = models.ForeignKey('sitestouristiques', related_name='visit_sites_touristiques', on_delete=models.CASCADE)
    # lieux_de_loisirs = models.ForeignKey('lieux_de_loisirs', related_name='visit_lieux_de_loisirs', on_delete=models.CASCADE)
    # event = models.ForeignKey('event', related_name='visit_event', on_delete=models.CASCADE) 
    # province = models.ForeignKey('province', related_name='visit_province', on_delete=models.CASCADE) 
    # quartiers = models.ForeignKey('quartiers', related_name='visit_quartiers', on_delete=models.CASCADE) 
    # churches = models.ForeignKey('churches', related_name='visit_churches', on_delete=models.CASCADE) 
    # market = models.ForeignKey('market', related_name='visit_market', on_delete=models.CASCADE) 
    # hospitals = models.ForeignKey('hospitals', related_name='visit_hospitals', on_delete=models.CASCADE) 
    # transport = models.ForeignKey('transport', related_name='visit_transport', on_delete=models.CASCADE) 
    # conference = models.ForeignKey('conference', related_name='visit_conference', on_delete=models.CASCADE) 
    # culture = models.ForeignKey('culture', related_name='visit_culture', on_delete=models.CASCADE) 
    # art = models.ForeignKey('art', related_name='visit_art', on_delete=models.CASCADE) 
    # guide = models.ForeignKey('guide', related_name='visit_guide', on_delete=models.CASCADE) 
    # service = models.ForeignKey("service", related_name='visit_service', on_delete=models.CASCADE) 
    # class Photo(models.Model):
    # champ pour stocker l'image
    # image = models.ImageField(upload_to='photos/')
    # # champ pour stocker la légende de l'image
    # caption = models.CharField(max_length=100)

class hotels(models.Model):
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    description = models.TextField(default="", blank=True)
    #service = models.ManyToManyField(service)
    # photo = models.ManyToManyField()
    video = models.FileField(upload_to='hotels_videos/', default='default.mp4',blank=True ,null=False)
    #reservation = models.ForeignKey("reservation" ,null=False, on_delete=models.CASCADE)
    contact = models.CharField(max_length=100,blank=True)
    stars = models.PositiveIntegerField(default=1, blank=True)
    #visit_count = models.PositiveIntegerField(default=0)
    mail = models.EmailField()
    url_site = models.URLField(blank=True)
    longitude = models.CharField(max_length=50, blank=True) 
    latitude = models.CharField(max_length=50, blank=True) 
    #chambre = models.PositiveIntegerField(default=0)
    #guide = models.ForeignKey('Guide',null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name 
####################################################################
# class Photo_guide(models.Model):
#     image = models.ImageField(upload_to='photos_guide')
#     guide = models.ForeignKey('Guide', related_name='photo_guides', on_delete=models.CASCADE)
# class Guide(models.Model):
#      name = models.CharField(max_length=100)
#      contact = models.IntegerField(default=0,blank=True)models.IntegerField()
#      stars = models.PositiveIntegerField(default=1)
#      mail = models.EmailField()
#      description = models.TextField()
#######################################################################
class Photo_service(models.Model):
    image = models.ImageField(upload_to='photos_service')
    service = models.ForeignKey('service', related_name='photo_service', on_delete=models.CASCADE)    

class service(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(default="", blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    #duration = models.TimeField()
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    # photo = models.ManyToManyField(Photo, related_name='visit_service')
    
    def __str__(self):
        return self.name
   
class Services_of_hotels(models.Model):
    hotel = models.ForeignKey(hotels ,null=False, on_delete=models.CASCADE)
    services = models.ForeignKey(service ,null=False, on_delete=models.CASCADE)
    
    # def _str_(self):
    #     return f'{self.hotel} - {self.services}'

    class Meta:
        unique_together =('hotel','services')

class Services_of_restaurants_bars(models.Model):
    restaurants_bars = models.ForeignKey("restaurant_bars",null=False, on_delete=models.CASCADE)
    services = models.ForeignKey(service ,null=False, on_delete=models.CASCADE)
    
    # def _str_(self):
    #     return f'{self.hotel} - {self.services}'

    class Meta:
        unique_together =('restaurants_bars','services')
#########################################################
class Guide(models.Model):
     name = models.CharField(max_length=100, blank=True)
    #  contact = models.CharField(max_length=100,blank=True)
      
     description = models.TextField(default="", blank=True)
     mail = models.EmailField()
    # hotel = models.ForeignKey(hotels, null=False,default=0, on_delete=models.CASCADE)
        
     def __str__(self):
        return self.name
     
class Photo_guide(models.Model):
    image = models.ImageField(upload_to='photos_guide', blank=True)
    guide = models.ForeignKey(Guide, related_name='photo_guide', on_delete=models.CASCADE)


class Guides_of_hotels(models.Model):
    hotel = models.ForeignKey(hotels ,null=False, on_delete=models.CASCADE)
    guides = models.ForeignKey(Guide ,null=False, on_delete=models.CASCADE)
    
    class Meta:
        unique_together =('hotel','guides')

class Guides_of_sitestouristiques(models.Model):
    sitestouristiques = models.ForeignKey('sitestouristiques' ,null=False, on_delete=models.CASCADE)
    guides = models.ForeignKey(Guide ,null=False, on_delete=models.CASCADE)
    
    class Meta:
        unique_together =('guides','sitestouristiques')

class Guides_of_provinces(models.Model):
    provinces = models.ForeignKey("province" ,null=False, on_delete=models.CASCADE)
    guides = models.ForeignKey(Guide ,null=False, on_delete=models.CASCADE)
    
    class Meta:
        unique_together =('provinces','guides')
##########################################################
class reservation(models.Model):
   # user = models.ForeignKey(user, on_delete=models.CASCADE)
    #service = models.ForeignKey(service, on_delete=models.CASCADE)
    booking_date = models.DateField( blank=True)
    booking_time = models.TimeField( blank=True)
    is_available = models.BooleanField(default=True, blank=True)
    #hotel = models.ForeignKey(hotels, null=False,default=0, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.name
    
class Reservations_of_services(models.Model):
    services_of_hotels = models.ForeignKey(Services_of_hotels ,null=False, on_delete=models.CASCADE)
    reservations = models.ForeignKey(reservation ,null=False, on_delete=models.CASCADE)
   
    class Meta:
        unique_together =('services_of_hotels','reservations')

class Reservations_of_restaurants(models.Model):
    restaurants_bars = models.ForeignKey('restaurant_bars' ,null=False, on_delete=models.CASCADE)
    reservations = models.ForeignKey(reservation ,null=False, on_delete=models.CASCADE)
   
    class Meta:
        unique_together =('restaurants_bars','reservations')

############################################################
class Photo_restaurant_bars(models.Model):
    image = models.ImageField(upload_to='photos_restaurant_bars')
    restaurant_bars= models.ForeignKey('restaurant_bars', related_name='photo_restaurant_bars', on_delete=models.CASCADE)  

class restaurant_bars(models.Model):
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="", blank=True)
    contact = models.CharField(max_length=100,blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_restaurant')
    video = models.FileField(upload_to='restaurant_bars_videos/', default='default.mp4')
    #service = models.ForeignKey(service, on_delete=models.CASCADE)
    #reservation = models.ForeignKey("reservation", on_delete=models.CASCADE)
     
    url_site = models.URLField(blank=True)
    mail = models.EmailField()  
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    # latitude = models.FloatField(null=True, blank=True) 

    def __str__(self):
        return self.name
    
############################################################
class Photo_food(models.Model):
    image = models.ImageField(upload_to='photos_food')
    food = models.ForeignKey('food', related_name='photo_food', on_delete=models.CASCADE)       

class food(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="", blank=True)
    address = models.CharField(max_length=100, blank=True)
    #stars = models.PositiveIntegerField(default=1)
    # photos = models.ManyToManyField(Photo, related_name='visit_food')
    contact = models.CharField(max_length=100,blank=True)
    url_site = models.URLField(blank=True)

    def __str__(self):
        return self.name   
########################################################
class Photo_nightclubs(models.Model):
    image = models.ImageField(upload_to='photos_nightclubs')
    nightclubs = models.ForeignKey('nightclubs', related_name='photo_nightclubs', on_delete=models.CASCADE)   

class nightclubs(models.Model):
    name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    stars = models.PositiveIntegerField( blank=True)
    description = models.TextField(default="", blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_bar')
    video = models.FileField(upload_to='nightclubs_videos/', default='default.mp4')
    #boissons = models.CharField(max_length=100)
    #service = models.ForeignKey(service, on_delete=models.CASCADE)
    contact = models.CharField(max_length=100,blank=True)
    mail = models.EmailField(max_length=254,)  
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    open_time = models.CharField(max_length=50, blank=True) 
    #close_time = models.TimeField(max_length=200)
    url_site = models.URLField(blank=True)
    prix_entrer = models.CharField(max_length=100, blank=True)
    #user

    def __str__(self):
       return self.name   
#######################################################
class Photo_sitestouristiques(models.Model):
    image = models.ImageField(upload_to='photos_sitestouristiques')
    sitestouristiques = models.ForeignKey('sitestouristiques', related_name='photo_sitestouristiques', on_delete=models.CASCADE)

class sitestouristiques(models.Model):
    name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="", blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_sites_touristiques')
    video = models.FileField(upload_to='sitestouristiques_videos/', default='default.mp4')
    open_time = models.DateTimeField( blank=True)
    guide = models.ForeignKey(Guide,null=True, on_delete=models.CASCADE)
    # contact_guide = models.PositiveIntegerField( blank=True)
    close_time = models.DateTimeField( blank=True)
    url_site = models.URLField(blank=True)
    contact = models.CharField(max_length=100,blank=True)
    mail = models.EmailField(max_length=254)
     
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    #guide = models.ForeignKey(Guide,null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name   
########################################################
class Photo_event(models.Model):
    image = models.ImageField(upload_to='photos_event')
    event = models.ForeignKey('event', related_name='photo_event', on_delete=models.CASCADE)  

class event(models.Model):
    name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="", blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_event')
    video = models.FileField(upload_to='event_videos/', default='default.mp4', blank=True)
    open_time = models.DateTimeField(max_length=200, blank=True)
    close_time = models.DateTimeField(max_length=200, blank=True)
     
    url_site = models.URLField(blank=True)
    contact = models.CharField(max_length=100,blank=True)
    is_national = models.BooleanField(default=True, blank=True)
    mail = models.EmailField(max_length=254)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return self.name  
############################################################
class Photo_lieux_de_loisirs(models.Model):
    image = models.ImageField(upload_to='photos_lieux_de_loisirs')
    lieux_de_loisirs = models.ForeignKey('lieux_de_loisirs', related_name='photo_lieux_de_loisirs', on_delete=models.CASCADE)

class lieux_de_loisirs(models.Model):
    name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="", blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_lieux_de_loisirs')
    video = models.FileField(upload_to='lieux_de_loisirs_videos/', default='default.mp4', blank=True)
    open_time = models.DateTimeField( blank=True)
    close_time = models.DateTimeField( blank=True)
    contact = models.CharField(max_length=100,blank=True)
     
    url_site = models.URLField(blank=True)
    mail = models.EmailField(max_length=254)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return self.name  
#################################################################
class Photo_province(models.Model):
    image = models.ImageField(upload_to='photos_province', blank=True)
    province = models.ForeignKey('province', related_name='photo_province', on_delete=models.CASCADE)

class province(models.Model):
    name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="", blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_province')
    video = models.FileField(upload_to='province_videos/', default='default.mp4', blank=True)
    # contact_guide = models.PositiveIntegerField()
    # taxi = models.CharField(max_length=200)
    # contact_taxi = models.PositiveIntegerField()
    contact_guide = models.PositiveIntegerField()
    url_site = models.URLField(blank=True)
    mail = models.EmailField(max_length=254)
     
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True) 
    guide = models.ForeignKey(Guide,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name  
############################################################
class Photo_quartiers(models.Model):
    image = models.ImageField(upload_to='photos_quartiers')
    quartiers = models.ForeignKey('quartiers', related_name='photo_quartiers', on_delete=models.CASCADE)

class quartiers(models.Model):
    name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="", blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_quartiers')
    guide = models.ForeignKey(Guide,null=True, on_delete=models.CASCADE)
    contact_guide = models.PositiveIntegerField( blank=True)
     
    contact = models.CharField(max_length=100,blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)  
    
    def _str_(self):
        return self.name 
#######################################################
class Photo_churches(models.Model):
    image = models.ImageField(upload_to='photos_churches')
    churches = models.ForeignKey('churches', related_name='photo_churches', on_delete=models.CASCADE)

class churches(models.Model):
    name = models.CharField(max_length=50, blank=True)
    description = models.TextField(default="", blank=True)
    address = models.CharField(max_length=300, blank=True)
    ville = models.CharField(max_length=300, blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_churches')
     
    video = models.FileField(upload_to='churches_videos/', default='default.mp4', blank=True)
    contact = models.CharField(max_length=100,blank=True)
    mail = models.EmailField(max_length=254)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return self.name  
#####################################################################
class Photo_market(models.Model):
    image = models.ImageField(upload_to='photos_market', blank=True)
    market = models.ForeignKey('market', related_name='photo_market', on_delete=models.CASCADE)  

class market(models.Model):
    name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="", blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_market')
    contact = models.CharField(max_length=100,blank=True)
    mail = models.EmailField(max_length=254)
     
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return self.name  
#############################################################
class Photo_hospitals(models.Model):
    image = models.ImageField(upload_to='photos_hospitals', blank=True)
    hospitals = models.ForeignKey('hospitals', related_name='photo_hospitals', on_delete=models.CASCADE)  

class hospitals(models.Model):
    name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="", blank=True)
    room = models.PositiveIntegerField( blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_hospitals')
    video = models.FileField(upload_to='hopital_videos/', default='default.mp4', blank=True)
    contact = models.CharField(max_length=100,blank=True)
    mail = models.EmailField(max_length=254) 
     
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True) 

    def __str__(self):
        return self.name  
##########################################################
class Photo_transport(models.Model):
    image = models.ImageField(upload_to='photos_transport')
    transport = models.ForeignKey('transport', related_name='photo_transport', on_delete=models.CASCADE)   

class transport(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    #description izokenerwa kubashaka kuri location
    description = models.CharField(max_length=200, blank=True)
      
    # photos = models.ManyToManyField(Photo, related_name='visit_transport')
    #video = models.FileField(upload_to='transport_videos/', default='default.mp4')
    contact = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.name 
     
class Tendance(models.Model):
    identification = models.CharField(max_length=200)
    image = models.ImageField(upload_to='tendances/') 
    origine = models.CharField(max_length=100)  
    page = models.CharField(max_length=100) 
    lien = models.URLField(blank=True)  

    def __str__(self):
        return f"Tendance: {self.page}"
    

class Information(models.Model):
    nom = models.CharField(max_length=100, blank=True)  
    description = models.TextField(blank=True)  
    contact = models.CharField(max_length=100, blank=True)  

    def __str__(self):
        return self.nom  





#################################################################
class Photo_conference(models.Model):
    image = models.ImageField(upload_to='photos_conference')
    conference = models.ForeignKey('conference', related_name='photo_conference', on_delete=models.CASCADE)   

class conference(models.Model):
    name = models.CharField(max_length=30, blank=True)
    organisateur = models.TextField(default="", blank=True)
    #ville = models.CharField(max_length=100)
    date_debut = models.DateTimeField( blank=True,null=True)
    address = models.CharField(max_length=300, blank=True)
    contact = models.CharField(max_length=100,blank=True)
    date_fin = models.DateTimeField( blank=True,null=True)
    description = models.TextField(default="", blank=True)
    stars = models.PositiveIntegerField(default=1, blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_conference')
    video = models.FileField(upload_to='conference_videos/', default='default.mp4')
    url_site = models.URLField(blank=True)
    mail = models.EmailField(max_length=254)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.name_complet} ({self.name_court})'

###################################################################
class Photo_culture(models.Model):
    image = models.ImageField(upload_to='photos_culture')
    culture = models.ForeignKey('culture', related_name='photo_culture', on_delete=models.CASCADE) 

class photo(models.Model):
    name = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='photo')
  


class culture(models.Model):
    name = models.CharField(max_length=100, blank=True)
    # description = models.TextField()
    address = models.CharField(max_length=300, blank=True)
    description = models.TextField(default="", blank=True)
    # photos = models.ManyToManyField(Photo, related_name='visit_culture' )
     
    video = models.FileField(upload_to='culture_videos/', default='default.mp4', blank=True)
    date_creation = models.DateField( blank=True)
    contact = models.CharField(max_length=100,blank=True)
    mail = models.EmailField(max_length=254)

    def __str__(self):
        return self.name
################################################################
class Photo_art(models.Model):
    image = models.ImageField(upload_to='photos_art')
    art = models.ForeignKey('art', related_name='photo_art', on_delete=models.CASCADE)

class art(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="", blank=True)
    auteur = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=100,blank=True)
     
    mail = models.EmailField()
    longitude = models.CharField(max_length=50, blank=True) 
    latitude = models.CharField(max_length=50, blank=True)
 
    def __str__(self):
        return self.name

    # photos = models.ManyToManyField(Photo, related_name='visit_art')

#########################################################
class Role(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True)
#####################################################################
class PageView(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    url = models.URLField( blank=True)
    image = models.ImageField()
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
##################################pages les plus vues#############################################
class view_guide(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
    
class view_art(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
    
class view_hotel(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
class view_restaurant_bars(models.Model):    
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
    
class view_food(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
    
class view_conference(models.Model):   
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
    
class view_event(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
  
class view_churches(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
class view_sitestouristiques(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
    
class view_market(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
    
class view_lieux_de_loisirs(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
class view_province(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
class view_quartiers(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
class view_hospital(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
class view_nightclubs(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
class view_culture(models.Model):
    page = models.CharField(max_length=100, blank=True)
    count = models.IntegerField(default=0, blank=True)
    image = models.ImageField()
    identification = models.IntegerField(default=0, blank=True)
    ordering = ['-count']
    #view_count = models.IntegerField(default=0)
    #last_viewed = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.page
    