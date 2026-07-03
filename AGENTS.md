# autenticaciondjango

Sistema de autenticación genérico con Django, roles y panel de usuario. Roles: Administrador, Empleado, Cliente. Orientado a negocios.

---

## Stack

| Componente | Versión |
|-----------|---------|
| Django | 3.2.25 (LTS, EOL) |
| Python | 3.10 |
| Base de datos | PostgreSQL |
| CSS | Tailwind CSS (CDN Play) |
| JS | Vanilla (sin framework) |
| API | Django REST Framework 3.14 + SimpleJWT 5.3.1 |
| Entorno | `django-environ` (.env) |

## Dependencias principales

- `Django==3.2.25`
- `django-environ==0.11.2`
- `psycopg2-binary==2.9.9`
- `Pillow==9.5.0` (sin usar aún)
- `django-model-utils==5.0.0` (sin usar aún)
- `djangorestframework==3.14.0`
- `djangorestframework-simplejwt==5.3.1`

## Estructura del proyecto

```
autenticaciondjango/
├── autenticaciondjango/        # Proyecto raíz
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── applications/
│   ├── home/                   # App landing page
│   │   ├── views.py            # IndexView (TemplateView)
│   │   └── urls.py             # app_name = 'app_home'
│   └── users/                  # App usuarios
│       ├── models.py           # User custom
│       ├── views.py            # Register, Login, Logout, UpdatePassword, Dashboard, ListaUsuarios, UserDetail, AdminEditUser, AdminResetPassword
│       ├── forms.py            # UserRegisterForm, LoginForm, UpdatePasswordForm, AdminEditUserForm, AdminResetPasswordForm
│       ├── urls.py             # app_name = 'app_users'
│       ├── admin.py            # UserAdmin personalizado
│       ├── managers.py         # UserManager
│       ├── mixins.py           # Permisos por rol (CBV)
│       ├── permissions.py      # Permisos DRF: IsAdmin, IsAdminOrEmployee, IsAdminOrClient
│       ├── serializers.py      # Serializers DRF + CustomTokenObtainPairSerializer
│       ├── views_api.py        # API views: UsuarioList, UsuarioDetail, UserMe, Register
│       └── migrations/
├── templates/
│   ├── base.html               # Layout con Tailwind
│   ├── home/index.html         # Landing page
│   ├── users/register.html     # Registro (admin completo / público solo Cliente)
│   ├── users/login.html        # Login
│   ├── users/dashboard.html    # Perfil propio
│   ├── users/cambiar_password.html
│   ├── users/lista_usuarios.html  # Lista con badge "Tú" y fila resaltada
│   ├── users/user_detail.html     # Detalle de usuario + botones editar/restablecer
│   ├── users/admin_edit_user.html # Editar datos (Admin)
│   ├── users/admin_reset_password.html # Restablecer contraseña (Admin)
│   └── include/header.html, footer.html
├── static/                     # Creado, vacío
├── media/                      # Creado, vacío
├── fixtures/                   # Creado, vacío
├── requirements.txt
├── .env (ignorado por git)
└── AGENTS.md
```

## Modelo User (`users.User`)

- Hereda de `AbstractBaseUser` + `PermissionsMixin`
- `USERNAME_FIELD = 'email'`
- `REQUIRED_FIELDS = ['first_name', 'last_name']`
- Campos: `email` (unique), `first_name`, `last_name`, `occupation`, `gender`, `date_birth`, `phone`, `is_staff`, `is_active`
- Usa `UserManager` (custom)

### Choices

**occupation**: `'0'` Administrador, `'1'` Empleado, `'2'` Cliente
**gender**: `'M'` Masculino, `'F'` Femenino, `'O'` Otro

## URLs

### `app_home` (namespace)
| URL | View | Name |
|-----|------|------|
| `/` | `IndexView` | `index` |

### `app_users` (namespace)
| URL | View | Name |
|-----|------|------|
| `/users/` | `DashboardView` | `dashboard` |
| `/users/register/` | `UserRegisterView` | `register` |
| `/users/login/` | `LoginUser` | `login` |
| `/users/logout/` | `LogoutView` | `logout` |
| `/users/update/` | `UpdatePasswordView` | `user-update` |
| `/users/lista/` | `ListaUsuariosView` | `user-list` |
| `/users/lista/<pk>/` | `UserDetailView` | `user-detail` |
| `/users/lista/<pk>/editar/` | `AdminEditUserView` | `user-edit` |
| `/users/lista/<pk>/password/` | `AdminResetPasswordView` | `user-reset-password` |

### API (JWT)
| URL | View | Name |
|-----|------|------|
| `POST /api/token/` | `TokenObtainPairView` | `api-token` |
| `POST /api/token/refresh/` | `TokenRefreshView` | `api-token-refresh` |
| `POST /api/token/verify/` | `TokenVerifyView` | `api-token-verify` |
| `POST /api/register/` | `RegisterAPIView` | `api-register` |
| `GET /api/usuarios/me/` | `UserMeAPIView` | `api-user-me` |
| `GET /api/usuarios/` | `UsuarioListAPIView` | `api-user-list` |
| `GET /api/usuarios/<pk>/` | `UsuarioDetailAPIView` | `api-user-detail` |

## Mixins de permisos

- `AdministradorPermisoMixin` — solo `occupation == '0'`
- `EmpleadoPermisoMixin` — Admin o Empleado
- `ClientePermisoMixin` — Admin o Cliente
- `login_url` → `app_users:login`

## Flujo de registro

- **Público** (no autenticado): ve "Registrarse" en el header → formulario SIN campo ocupación → se crea como **Cliente** → auto-login + mensaje flash
- **Admin** (logueado con `occupation == '0'`): ve "Nuevo usuario" en el header → formulario CON campo ocupación → puede elegir Admin/Empleado/Cliente

## Protección de superusuarios

- `ListaUsuariosView`: filtra `is_superuser=False` (no aparecen en la lista)
- `UserDetailView`, `AdminEditUserView`, `AdminResetPasswordView`: devuelven `Http404` si el usuario es superuser

## Settings relevantes

```python
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'app_users:login'
LOGIN_REDIRECT_URL = 'app_users:dashboard'
LOGOUT_REDIRECT_URL = 'app_users:login'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# DRF + JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_OBTAIN_SERIALIZER': 'applications.users.serializers.CustomTokenObtainPairSerializer',
}
```

## Throttling (protección fuerza bruta)

- `AnonRateThrottle` global: **10 requests/hora** por IP para endpoints públicos (`/api/token/`)
- Protege contra ataques de fuerza bruta sobre el login JWT
- Configurable en `settings.py` → `DEFAULT_THROTTLE_RATES['anon']`

## Estilo y convenciones

- **CSS**: Tailwind CDN en `base.html`, estilos inline con clases utilitarias
- **Navbar**: menú responsive con vanilla JS toggle (sin Alpine.js ni jQuery)
- **Formularios**: widgets con clase `INPUT_CLASS` definida en `forms.py`
- **Encoding**: todos los textos en español, UTF-8
- **Mensajes flash**: mapeo de `message.tags` a colores Tailwind (success → verde, error → rojo, etc.)
- **Logout**: mediante POST (CSRF protegido)

## Pendientes / Mejoras futuras

- Migrar Django 3.2 → 4.2 LTS o 5.0 (EOL desde abril 2024)
- Remover `USE_L10N` de settings (deprecado)
- Mover Tailwind CDN a build estático con CLI para producción
- Agregar tests
- Implementar lógica de negocio en `services.py`
- Usar `Pillow` para avatar/foto de perfil
- Corregir typo `procesors` en comentario de settings

## Comandos útiles

```bash
# Activar entorno
venv\Scripts\activate

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Admin
python manage.py createsuperuser

# Estáticos
python manage.py collectstatic
```