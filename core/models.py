from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    biografia = models.CharField(max_length=500, blank=True)
    
    seguindo = models.ManyToManyField('self', symmetrical=False, related_name='seguidores', blank=True)
    
    def __str__(self):
        return self.username


class Postagem(models.Model):
    autor = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True)
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    autor = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True)
    post_original = models.ForeignKey('Postagem', on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentário de {self.autor} em {self.post_original}'


class Interacao(models.Model):
    autor = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True)
    
    post = models.ForeignKey('Postagem', on_delete=models.CASCADE, null=True, blank=True)
    comentario = models.ForeignKey('Comentario', on_delete=models.CASCADE, null=True, blank=True)
    
    tipo = models.CharField(max_length=20)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo} de {self.autor}'