from django.contrib import admin
from .models import Auction, Category, Bid, Rating, Comment

# Registro básico de todos los modelos para que sean gestionables desde el admin de Django
admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Rating)
admin.site.register(Comment)