import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from .models import Usuario


def gerar_token(usuario):
    horario = datetime.now(timezone.utc)
    payload = {
        "user_id": usuario.id,
        "iat": horario,
        "exp": horario + timedelta(days=7)
    }

    return jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")


def obter_usuario_logado(request):
    header = request.headers.get("Authorization")
    if not header or not header.startswith("Bearer "):
        return None, "Sem token de autenticação ou formato errado!"

    token = header.split("Bearer ", 1)[1].strip()
    if not token:
        return None, "Token inválido."

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        usuario = Usuario.objects.get(id=payload["user_id"])
        return usuario, None
    except jwt.ExpiredSignatureError:
        return None, "Token expirado."
    except jwt.InvalidTokenError:
        return None, "Token inválido ou adulterado."
    except Usuario.DoesNotExist:
        return None, "Usuário não existe mais!"