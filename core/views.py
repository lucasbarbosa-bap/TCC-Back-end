from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
