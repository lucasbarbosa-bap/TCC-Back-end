from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Postagem, Comentario, Interacao

admin.site.register(Usuario, UserAdmin)
admin.site.register(Postagem)
admin.site.register(Comentario)
admin.site.register(Interacao)