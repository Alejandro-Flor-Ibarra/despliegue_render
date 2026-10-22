# Despliegue del proyecto

## Inicio local

Clona el repositorio y entra a la carpeta del proyecto:

```bash
git clone <URL_DEL_REPOSITORIO>
cd despliegue_render
```

## Variables de entorno

| Windows | Linux |
| --- | --- |
| `Copy-Item .env.example .env` | `cp .env.example .env` |

Completa en `.env` los valores para tu entorno local. No agregues secretos reales a `.env.example` ni subas `.env` al repositorio.

## Entorno virtual e inicio

| Windows | Linux |
| --- | --- |
| `python -m venv .venv`<br>`.venv\Scripts\Activate.ps1`<br>`pip install -r requirements.txt`<br>`python manage.py migrate`<br>`python manage.py runserver` | `python3 -m venv .venv`<br>`source .venv/bin/activate`<br>`pip install -r requirements.txt`<br>`python manage.py migrate`<br>`python manage.py runserver` |

Abre http://127.0.0.1:8000 en el navegador.