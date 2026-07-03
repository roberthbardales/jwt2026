# JWT 2026

Sistema de autenticación con Django, REST Framework, Tailwind CSS y JWT.

## Stack

- Django 3.2.25
- Python 3.10
- PostgreSQL
- Tailwind CSS (CDN)
- Django REST Framework 3.14.0
- SimpleJWT 5.3.1

## Endpoints JWT

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/token/` | Obtener access + refresh token | Pública |
| POST | `/api/token/refresh/` | Refrescar access token | Pública |
| POST | `/api/token/verify/` | Verificar token | Pública |
| POST | `/api/register/` | Registrar usuario (Cliente por defecto) | Pública |
| GET | `/api/usuarios/me/` | Perfil del usuario autenticado | Bearer Token |
| GET | `/api/usuarios/` | Listar usuarios (solo Admin) | Bearer Token |
| GET | `/api/usuarios/<id>/` | Detalle de usuario (solo Admin) | Bearer Token |

## Probar JWT con curl

```bash
# 1. Obtener token
curl -X POST http://localhost:8000/api/token/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@ejemplo.com\",\"password\":\"tucontraseña\"}"

# 2. Obtener perfil propio
curl http://localhost:8000/api/usuarios/me/ ^
  -H "Authorization: Bearer eyJ..."

# 3. Refrescar token
curl -X POST http://localhost:8000/api/token/refresh/ ^
  -H "Content-Type: application/json" ^
  -d "{\"refresh\":\"eyJ...\"}"

# 4. Registrar usuario
curl -X POST http://localhost:8000/api/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@test.com\",\"first_name\":\"Test\",\"last_name\":\"User\",\"gender\":\"M\",\"password\":\"Pass1234!\"}"

# 5. Listar usuarios (admin)
curl http://localhost:8000/api/usuarios/ ^
  -H "Authorization: Bearer eyJ..."
```

## Token payload

El access token incluye: `user_id`, `email`, `first_name`, `last_name`, `occupation`, `gender`. Decodificar en [jwt.io](https://jwt.io).

## Web (sesiones)

La autenticación web por sesiones sigue funcionando en paralelo sin cambios.
