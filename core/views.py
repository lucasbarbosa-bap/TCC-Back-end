from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Postagem, Usuario
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
def gerenciar_postagens(request):
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
    
    elif request.method == 'POST':
        if request.body:
            resposta = json.loads(request.body)
            informacoes_postagem = {
                "titulo": resposta.get('titulo'),
                "conteudo": resposta.get('conteudo'),
                "autor_id": resposta.get('autor'),
            }
            Postagem.objects.create(**informacoes_postagem)
            return JsonResponse({"mensagem": "Postagem criada com sucesso!"}, status=201)
        else:
            return JsonResponse({"mensagem": "Insira informações válidas!"}, status=400)

    
    else:
        return JsonResponse({"erro": "Método não permitido. Utilize GET ou POST."}, status=405)

def gerenciar_usuarios(request, id):
    if request.method == 'GET':
        try:
            usuario = Usuario.objects.get(id=id)
            return JsonResponse({"mensagem": usuario.username}, status=200)
        except Usuario.DoesNotExist:
            return JsonResponse({"erro": "Usuário não encontrado."}, status=404)
    else:
        return JsonResponse({"erro": "Método não permitido. Utilize GET."}, status=405)