# Prueba de JWT

## 1. Activar entorno y migraciones

```powershell
venv\Scripts\activate
python manage.py migrate
```

## 2. Crear superuser (si no tienes)

```powershell
python manage.py createsuperuser
```

## 3. Iniciar servidor

```powershell
python manage.py runserver
```

## 4. Probar endpoints

### Obtener token (login)

```powershell
$token = curl -Uri "http://127.0.0.1:8000/api/token/" -Method POST -Body (@{email="admin@mail.com"; password="tu_password"} | ConvertTo-Json) -ContentType "application/json" | Select-Object -ExpandProperty Content | ConvertFrom-Json

$token.access
```

### Ver mi perfil

```powershell
curl -Uri "http://127.0.0.1:8000/api/usuarios/me/" -Headers @{Authorization="Bearer $($token.access)"} | Select-Object -ExpandProperty Content
```

### Listar usuarios (solo Admin)

```powershell
curl -Uri "http://127.0.0.1:8000/api/usuarios/" -Headers @{Authorization="Bearer $($token.access)"} | Select-Object -ExpandProperty Content
```

### Registrar cliente nuevo (público)

```powershell
curl -Uri "http://127.0.0.1:8000/api/register/" -Method POST -Body (@{email="cliente@mail.com"; password="Cliente12345"; first_name="Juan"; last_name="Perez"; gender="M"; phone="999888777"} | ConvertTo-Json) -ContentType "application/json"
```

### Refrescar token

```powershell
curl -Uri "http://127.0.0.1:8000/api/token/refresh/" -Method POST -Body (@{refresh=$token.refresh} | ConvertTo-Json) -ContentType "application/json"
```

### Verificar token

```powershell
curl -Uri "http://127.0.0.1:8000/api/token/verify/" -Method POST -Body (@{token=$token.access} | ConvertTo-Json) -ContentType "application/json"
```
