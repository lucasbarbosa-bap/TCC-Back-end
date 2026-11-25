from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Postagem, Usuario, Comentario, Interacao
import json
import cloudinary.uploader

# Create your views here.

User = get_user_model()

def upload_midia(arquivo, pasta, aceita_video=False, tamanho_max_mb=5, redimensionar=False):
    if arquivo.size > tamanho_max_mb * 1024 * 1024:
        return None, f"Arquivo grande demais (máximo {tamanho_max_mb}MB) >o<"
    
    tipos_permitidos = ['image/jpg', 'image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if aceita_video:
        tipos_permitidos += ['video/mp4', 'video/webm', 'video/quicktime']

    if arquivo.content_type not in tipos_permitidos:
        return None, "Tipo de arquivo inválido >~<"
    opcoes = {
        "folder": f"tcc/{pasta}",
        "resource_type": "auto" if aceita_video else "image"
    }
    if redimensionar:
        opcoes["transformation"] = [{"width": 500, "height": 500, "crop": "limit"}]

    try:
        upload = cloudinary.uploader.upload(arquivo, **opcoes)
        return upload['secure_url'], None
    except Exception as e:
        print(f"Erro no upload do Cloudinary: {e}") #Para debug no console
        return None, "Erro ao processar a mídia >~<"

# Formatar as requisições PUT e PATCH
def ler_dados_atualizacoes(request):
    if request.content_type == 'multipart/form-data':
        dados, arquivos = request.parse_file_upload(request.META, request)
        return dados, arquivos
    elif request.content_type == 'application/json' and request.body:
        return json.loads(request.body), {}
    return {}, {}

@csrf_exempt #Tirar trava de formulário padrão do django

def fazer_login(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        usuario = authenticate(username=dados.get('username'), password=dados.get('password'))
        if usuario:
            return JsonResponse({
                "mensagem": "Login Feito UwU!", 
                "id": usuario.id, 
                "username": usuario.username, 
                "avatar": usuario.foto_perfil, 
                "biografia": usuario.biografia 
                }, status=200)
        else:
            return JsonResponse({"mensagem": "Credenciais inválidas >_<!"}, status=401)
    
    else:
        return JsonResponse({"erro": "Método não permitido. Utilize POST."}, status=405)

@csrf_exempt

def fazer_cadastro(request):
    if request.method == 'POST':
            if request.POST:
                username = request.POST.get('username')
                email = request.POST.get('email')
                password = request.POST.get('password')
                avatar = ""

                if User.objects.filter(username=username).exists():
                    return JsonResponse({"erro": "Username ja existe!"}, status=400)
                if request.FILES.get('avatar'):
                    arquivo = request.FILES.get('avatar')
                    avatar, erro = upload_midia(arquivo, pasta="avatares", redimensionar=True)
                    if erro:
                        return JsonResponse({"erro": erro}, status=400)

                novo_usuario = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    foto_perfil=avatar
                )
                return JsonResponse({"mensagem": "Usuario cadastrado com sucesso >~<", "id": novo_usuario.id}, status=201)
            else:
                return JsonResponse({"erro": "Sem corpo"}, status=400)
    else:
        return JsonResponse({"erro": "Método não permitido. Utilize POST."}, status=405)

@csrf_exempt
def gerenciar_postagens(request):
    if request.method == 'GET':
        postagens_banco = Postagem.objects.all().order_by('-data_criacao')
        postagens_filtradas = []

        for postagem in postagens_banco:
            postagens_filtradas.append({
                "id": postagem.id,
                "titulo": postagem.titulo,
                "autor": {"id": postagem.autor.id, "nome": postagem.autor.username, "avatar": postagem.autor.foto_perfil} if postagem.autor else None,
                "data_criacao": postagem.data_criacao,
                "conteudo": postagem.conteudo,
                "midia": postagem.midia,
                "curtidas": Interacao.objects.filter(post=postagem, tipo='like').count(),
                "compartilhamentos": Interacao.objects.filter(post=postagem, tipo='share').count(),
                "comentarios": Comentario.objects.filter(post_original=postagem).count()
            })
        return JsonResponse({"Postagens": postagens_filtradas}, status=200)
    
    elif request.method == 'POST':
        if request.POST:
            informacoes_postagem = {
                "titulo": request.POST.get('titulo'),
                "conteudo": request.POST.get('conteudo'),
                "autor_id": request.POST.get('autor'),
                "midia": []
            }
            if not informacoes_postagem["titulo"] or not informacoes_postagem["conteudo"]:
                return JsonResponse({"erro": "campos insuficientes >.<"}, status=400)
            arquivos = request.FILES.getlist('midia')
            if  arquivos:
                if len(arquivos) > 10:
                    return JsonResponse({"erro": "Muitas mídias >O<"}, status=400)
                midias = []

                for arquivo in arquivos:
                    midia, erro = upload_midia(arquivo, pasta="posts", aceita_video=True, tamanho_max_mb=20)
                    if erro:
                        return JsonResponse({"erro": erro}, status=400)
                    midias.append(midia)

                informacoes_postagem["midia"] = midias
            
            Postagem.objects.create(**informacoes_postagem)
            return JsonResponse({"mensagem": "Postagem criada com sucesso!"}, status=201)
        else:
            return JsonResponse({"mensagem": "Insira informações válidas!"}, status=400)
    
    else:
        return JsonResponse({"erro": "Método não permitido. Utilize GET ou POST."}, status=405)

@csrf_exempt
def detalhar_postagem(request, id):
    try:
        post = Postagem.objects.get(id=id)
    except Postagem.DoesNotExist:
        return JsonResponse({"erro": "Post não encontrado."}, status=404)
    if request.method == 'GET':
        post_informacoes =  {
                "id": post.id,
                "titulo": post.titulo,
                "autor": {"id": post.autor.id, "nome": post.autor.username, "avatar": post.autor.foto_perfil} if post.autor else None,
                "data_criacao": post.data_criacao,
                "conteudo": post.conteudo,
                "midia": post.midia,
                "curtidas": Interacao.objects.filter(post=post, tipo='like').count(),
                "compartilhamentos": Interacao.objects.filter(post=post, tipo='share').count(),
                "comentarios": Comentario.objects.filter(post_original=post).count()
            }
        return JsonResponse({"Post": post_informacoes}, status=200)

    else:
        return JsonResponse({"erro": "Método não permitido. Utilize GET."}, status=405)


@csrf_exempt
def gerenciar_usuarios(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        return JsonResponse({"erro": "Usuário não encontrado."}, status=404)
    
    if request.method == 'GET':
            postagens_banco = Postagem.objects.filter(autor=usuario).order_by('-data_criacao')
            posts_usuario= []

            for postagem in postagens_banco:
                postagem_filtrada = {
                    "id": postagem.id,
                    "titulo": postagem.titulo,
                    "conteudo": postagem.conteudo,
                    "midia": postagem.midia,
                    "data_criacao": postagem.data_criacao,
                    "curtidas": Interacao.objects.filter(post=postagem, tipo='like').count(),
                    "compartilhamentos": Interacao.objects.filter(post=postagem, tipo='share').count(),
                    "comentarios": Comentario.objects.filter(post_original=postagem).count()
                }
                posts_usuario.append(postagem_filtrada)

            return JsonResponse({"mensagem": {
                "id": usuario.id,
                "username": usuario.username, 
                "avatar": usuario.foto_perfil, 
                "biografia": usuario.biografia, 
                "seguidores": usuario.seguidores.count(),
                "seguindo": usuario.seguindo.count(),
                "posts": posts_usuario
                }}, status=200)
        
    elif request.method == 'PUT' or request.method == 'PATCH':
        dados, arquivo = ler_dados_atualizacoes(request)
        if not dados and not arquivo:
            return JsonResponse({"erro": "Envie os dados para atualiza!"}, status=400)
        if dados.get('username'):
             if Usuario.objects.filter(username=dados.get('username')).exclude(id=usuario.id).exists():
                return JsonResponse({"erro": "Username já existe >x<!"}, status=400)
             usuario.username = dados.get('username')
        if arquivo.get('avatar'):
            avatar, erro = upload_midia(arquivo.get('avatar'),  pasta="avatares", redimensionar=True)
            if erro:
                return JsonResponse({"erro": erro}, status=400)
            usuario.foto_perfil = avatar
        if dados.get('biografia') is not None:
            usuario.biografia = dados.get('biografia')
        usuario.save()
        return JsonResponse({"mensagem": "Informações atualizadas com sucesso >o<!"}, status=200)
    
    elif request.method == 'DELETE':
        usuario.delete()
        return JsonResponse({"mensagem": "Usuário deletado com sucesso!"}, status=200)
    
    else:
        return JsonResponse({"erro": "Método não permitido. Utilize GET, PATCH OU PUT."}, status=405)

@csrf_exempt
def gerenciar_comentarios(request, id_post):
    try:
        post = Postagem.objects.get(id=id_post)
    except Postagem.DoesNotExist:
        return JsonResponse({"erro": "Post não encontrado."}, status=404)
    
    if request.method == 'POST':
        if request.POST:
            informacoes_comentario = {
                "autor_id": request.POST.get('autor'),
                "post_original": post,
                "conteudo": request.POST.get('conteudo'),
                "midia": [],
            }
            if not informacoes_comentario["conteudo"]:
                return JsonResponse({"erro": "campos insuficientes >.<"}, status=400)
            arquivos = request.FILES.getlist('midia')
            if arquivos:
                if len(arquivos) > 5:
                    return JsonResponse({"erro": "Muitas mídias >O<"}, status=400)
                midias = []
                for arquivo in arquivos:
                    midia, erro = upload_midia(arquivo, pasta="comentarios")
                    if erro:
                        return JsonResponse({"erro": erro}, status=400)
                    midias.append(midia)
                informacoes_comentario["midia"] = midias
            Comentario.objects.create(**informacoes_comentario)
            return JsonResponse({"mensagem": "Comentário criado com sucesso!"}, status=201)
        else:
            return JsonResponse({"mensagem": "Insira informações válidas!"}, status=400)
        
    elif request.method == 'GET':
        comentarios_banco = Comentario.objects.filter(post_original=post).order_by('data_criacao')
        comentarios_filtrados = []

        for comentario in comentarios_banco:
            comentarios_filtrados.append({
                "autor": {"id": comentario.autor.id, "nome": comentario.autor.username, "avatar": comentario.autor.foto_perfil} if comentario.autor else None,
                "id": comentario.id,
                "post_original": comentario.post_original.id,
                "conteudo": comentario.conteudo,
                "data_criacao": comentario.data_criacao,
                "midia": comentario.midia,
                "curtidas": Interacao.objects.filter(comentario=comentario, tipo='like').count(),
                "compartilhamentos": Interacao.objects.filter(comentario=comentario, tipo='share').count(),
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