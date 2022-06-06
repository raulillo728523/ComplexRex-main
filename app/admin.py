from django.contrib import admin
from .models import Marca, UserComplex, Producto

# Register your models here.

class userComplexList(admin.ModelAdmin):
    list_display = ["nombre","apellidos","correo","status","fechaCreacion","residencia","QR"]
    search_fields = ["nombre","correo"]

admin.site.register(UserComplex, userComplexList)
