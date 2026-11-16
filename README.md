# SmartBooking API

API para la app de reservas del coworking. Una sola sala. Hecha con Django y Django REST Framework.

No hay frontend Angular en este repo. Para ver los datos uso el admin de Django (`/admin/`).

## Como levantarla

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py crear_demo
python manage.py runserver
```

Admin: http://127.0.0.1:8000/admin/
Usuario `admin` / `Admin123!`

La base por defecto es SQLite (archivo `db.sqlite3`, no se sube a git). Es un motor relacional y alcanza para la defensa. Si quieren MySQL, en el `.env` pongan `DB_ENGINE=mysql` y completen los datos. El script esta en `docs/schema.sql`. El DER esta en el repo de la app.

## Endpoints

| Metodo | Ruta | Quien |
|---|---|---|
| POST | /api/auth/register/ | publico |
| POST | /api/auth/login/ | publico |
| POST | /api/auth/refresh/ | con refresh |
| POST | /api/auth/logout/ | autenticado, body `{"refresh": "..."}` |
| GET PUT | /api/perfil/ | autenticado |
| GET POST | /api/reservas/ | autenticado |
| GET PUT PATCH DELETE | /api/reservas/{id}/ | duenio o admin |
| GET PATCH | /api/usuarios/ y /api/usuarios/{id}/ | solo admin |

El token va en `Authorization: Bearer <access>`.

## Reglas

- RN01 no se pueden superponer dos reservas el mismo dia
- RN02 no se reserva en el pasado
- RN03 la hora de fin es posterior a la de inicio
- RN04 un usuario solo ve y toca sus reservas
- RN05 solo el admin gestiona usuarios y ve reservas de otros

## Pruebas

```bash
python manage.py test
```
