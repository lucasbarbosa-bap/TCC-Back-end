from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Postagem, Usuario, Comentario, Interacao
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

@csrf_exempt
def gerenciar_comentarios(request):
    if request.method == 'POST':
        if request.body:
            resposta = json.loads(request.body)
            informacoes_comentario = {
                "autor_id": resposta.get('autor'),
                "post_original_id": resposta.get('post_original'),
                "conteudo": resposta.get('conteudo'),
            }
            Comentario.objects.create(**informacoes_comentario)
            return JsonResponse({"mensagem": "Comentário criada com sucesso!"}, status=200)
        else:
            return JsonResponse({"mensagem": "Insira informações válidas!"}, status=400)
        
    elif request.method == 'GET':
         comentarios_banco = Comentario.objects.all()
         comentarios_filtrados = []
         
         for comentario in comentarios_banco:
             comentarios_filtrados.append({
                "autor": {"id": comentario.autor.id, "nome": comentario.autor.username},
                "post_original": comentario.post_original.id,
                "conteudo": comentario.conteudo,
                "data_criacao": comentario.data_criacao,
             })
         return JsonResponse({"Comentarios": comentarios_filtrados}, status=200)
    
    else:
        return JsonResponse({"erro": "Método não permitido. Utilize GET ou POST."}, status=405)

@csrf_exempt
def gerenciar_interacoes(request):
    if request.method == 'POST':
        if request.body:
            resposta = json.loads(request.body)
            informacoes_interacao = {
                "autor_id": resposta.get('autor'),
                "post_id": resposta.get('post'),
                "comentario_id": resposta.get('comentario'),
                "tipo": resposta.get('tipo'),
            }
            Interacao.objects.create(**informacoes_interacao)
            return JsonResponse({"mensagem": "Interação criada com sucesso!"}, status=201)
        else:
            return JsonResponse({"mensagem": "Insira informações válidas!"}, status=400)
        
    elif request.method == 'GET':
        Interacoes_banco = Interacao.objects.all()
        Interacoes_filtradas = []

        for interacao in Interacoes_banco:
            Interacoes_filtradas.append({
                "autor_id": interacao.autor_id,
                "post_id": interacao.post_id,
                "comentario_id": interacao.comentario_id,
                "tipo": interacao.tipo,
            })

        return JsonResponse({"Interações": Interacoes_filtradas}, status=200)
    else:
        return JsonResponse({"erro": "Método não permitido. Utilize GET ou POST."}, status=405)