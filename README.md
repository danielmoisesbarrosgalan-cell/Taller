# Taller Mecánico - Django

Sistema para un taller automotriz: clientes y sus vehículos, mecánicos, órdenes de
servicio y los servicios realizados en cada orden con su precio.
Sigue la misma estructura del proyecto *Gestor de Artículos* (apps, `models`,
`forms`, `views`, `urls`, `templates`, Bootstrap 5, 404 personalizada, pruebas).

## Modelo de datos

| Tabla | Relaciones |
| --- | --- |
| `Cliente` | 1:N `Vehiculo` |
| `Vehiculo` | 1:N `OrdenServicio` |
| `Mecanico` | 1:N `OrdenServicio` |
| `OrdenServicio` | N:M `Servicio` mediante `DetalleOrden` (débil: precio, observación) |

## Actores (grupos de Django)

| Rol | Permisos |
| --- | --- |
| Administrador | CRUD de todo |
| Recepcionista | CRUD de clientes y vehículos; abre/edita órdenes y agrega servicios |
| Mecánico | Ve sus órdenes, agrega/quita servicios y cambia el estado |
| Cliente | Solo consulta las órdenes de sus vehículos |

## Ejecutar

```bash
python -m venv entorno
entorno\Scripts\activate        # Linux/Mac: source entorno/bin/activate
pip install -r requirements.txt
python manage.py makemigrations cliente vehiculo mecanico servicio orden
python manage.py migrate
python manage.py crear_demo      # roles, usuarios y datos de ejemplo
python manage.py runserver
```

Abrir http://127.0.0.1:8000/ y entrar con:

| Usuario | Clave | Rol |
| --- | --- | --- |
| admin | admin123 | Administrador |
| recepcion | recepcion123 | Recepcionista |
| mecanico1 | mecanico123 | Mecánico |
| cliente1 | cliente123 | Cliente |

Pruebas: `python manage.py test`
