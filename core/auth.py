import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings

def gerar_token(usuario):
    horario = datetime.now(timezone.utc)
    payload = {
        "user_id": usuario.id,
        "iat": horario,
        "exp":horario + timedelta(days=7)
    }

    return jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")