# Sistema de Asistencias - Iglesia V2

Sistema web modular para el manejo de asistencias de una iglesia, desarrollado con Django y PostgreSQL.

## Tecnologías

- **Backend:** Python 3.12 + Django 6.x
- **Base de datos:** PostgreSQL
- **Frontend:** Bootstrap 5.3 + Bootstrap Icons

## Estructura del proyecto

```
Sistema Iglesia Refactor/
├── config/                  # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # Usuarios, roles, login, dashboards
├── miembros/                # Gestión de miembros
├── eventos/                 # Eventos y asistencias
├── visitas/                 # Portal del pastor y visitas
├── reportes/                # Reportes de asistencia
├── core/                    # Configuración del sitio y mantenimiento
├── templates/               # Templates HTML
├── static/                  # Archivos estáticos
├── media/                   # Archivos subidos
├── .env.example
├── requirements.txt
└── manage.py
```

## Requisitos previos

- [Python 3.12+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Daniel-0556/sistema-iglesia-v2.git
cd sistema-iglesia-v2
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv myvenv
```

**Windows:**
```bash
myvenv\Scripts\activate
```

**Mac/Linux:**
```bash
source myvenv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia `.env.example` y renómbralo `.env`:

```bash
copy .env.example .env
```

Edita `.env` con tus credenciales:

```
SECRET_KEY=genera-una-key-segura
DEBUG=True
DB_NAME=sistema_iglesia_v2
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

Para generar una `SECRET_KEY` segura:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Crear la base de datos en PostgreSQL

En pgAdmin crea una base de datos llamada `sistema_iglesia_v2`, o en psql:

```sql
CREATE DATABASE sistema_iglesia_v2;
```

### 6. Correr las migraciones

```bash
python manage.py migrate
```

### 7. Crear el superusuario

```bash
python manage.py createsuperuser
```

### 8. Configuración inicial desde el admin

Entra a `http://127.0.0.1:8000/admin` y crea en este orden:

1. **Iglesia** — nombre y logo
2. **Configuración del sitio** — nombre del sistema y colores
3. **Modo mantenimiento** — créalo con `activo = False`
4. **Roles** — Supervisor, Secretaria, Digitador, Pastor, Presidente
5. **Un usuario Supervisor** — asígnale iglesia y rol

### 9. Correr el servidor

```bash
python manage.py runserver
```

Abre en tu navegador: `http://127.0.0.1:8000`

---

## Roles del sistema

| Rol | Permisos |
|-----|----------|
| **Superusuario** | Acceso total. Configuración global del sistema |
| **Supervisor** | Gestiona usuarios, miembros, eventos y solicitudes de su iglesia |
| **Secretaria** | Agrega y edita miembros. Para eliminar necesita autorización del Supervisor |
| **Digitador** | Solo registra asistencias en los eventos |
| **Pastor** | Visualiza asistencias y gestiona visitas a miembros con poca asistencia |
| **Presidente** | Solo visualización general. No puede modificar nada |

---

## Ver en dispositivos móviles

1. Encuentra tu IP con `ipconfig` (Windows)
2. Agrega tu IP a `ALLOWED_HOSTS` en `settings.py`
3. Corre el servidor con:

```bash
python manage.py runserver 0.0.0.0:8000
```

4. Desde el celular entra a `http://TU-IP:8000`

---

## Notas importantes

- El archivo `.env` nunca debe subirse a GitHub
- La carpeta `media/` contiene logos — respaldarla regularmente
- Para producción cambiar `DEBUG=False` en el `.env`
