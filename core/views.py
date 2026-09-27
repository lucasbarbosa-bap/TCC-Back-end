from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Postagem
import json

# Create your views here.

@csrf_exempt #Tirar trava de formulário padrão do django

def fazer_login(request):
    if request.method == 'POST':
        resposta = json.loads(request.body)
        autenticado = authenticate(username=resposta.get('username'), password=resposta.get('password'))
        if autenticado:
            return JsonResponse({"mensagem": "Login Feito UwU!"}, status=200)
        else:
            return JsonResponse({"mensagem": "Credenciais inválidas >_<!"}, status=401)
    
    else:
        return JsonResponse({"erro": "Método não permitido. Utilize POST."}, status=405)

@csrf_exempt
def ver_postagens(request):
    if request.method == 'GET':
        postagens_banco = Postagem.objects.all()
        postagens_filtradas = []

        for postagem in postagens_banco:
            postagens_filtradas.append({
                "id": postagem.id,
                "titulo": postagem.titulo,
                "autor": {"id": postagem.autor.id, "nome": postagem.autor.username},
                "data_criacao": postagem.data_criacao,
                "conteudo": postagem.conteudo,

            })
        return JsonResponse({"Postagens": postagens_filtradas}, status=200)

    else:
        return JsonResponse({"erro": "Método não permitido. Utilize GET."}, status=405)
