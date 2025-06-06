# API de Asignación de Servicios de Domicilio

## Descripción

Este proyecto implementa una API backend para asignar servicios de domicilio, seleccionando automáticamente el conductor disponible más cercano al cliente.

Permite:

- CRUD de Direcciones.
- CRUD de Conductores.
- Solicitar un servicio.
- Asignación automática del conductor más cercano.
- Marcar un servicio como completado.
- Protección de API mediante JWT.

---

## Tecnologías utilizadas

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- Docker y Docker Compose
- Poetry
- Faker (para datos falsos)

---

## Configuración local (opcional, sin Docker)

> Requiere instalar Python 3.12, PostgreSQL y Poetry.

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

---

## Levantar el proyecto con Docker

1. Clonar el repositorio:

```bash
git clone https://github.com/jguerrero10/alfredApp.git
cd alfredApp
```

2. Levantar contenedores:

```bash
docker-compose up --build
```

3. Acceder a la API:

```
http://localhost:8000/api/
```

---
## Creación de superusuario (admin)

Para gestionar los modelos a través del panel de administración de Django (`/admin/`), es necesario crear un superusuario.

Puedes hacerlo ejecutando:

```bash
docker-compose exec web python manage.py createsuperuser
```

---
##  Documentación de la API

La API cuenta con documentación automática generada con `drf-spectacular`.

### Endpoints de documentación disponibles:

| URL | Descripción |
|:----|:------------|
| `/api/docs/` | Documentación interactiva Swagger UI |
| `/api/redoc/` | Documentación en formato Redoc |
| `/api/schema/` | Esquema OpenAPI 3 en formato JSON |
 
Desde `/api/docs/` se pueden ejecutar y probar directamente los endpoints protegidos con JWT.

La documentación se genera automáticamente a partir de los serializers, views y rutas registradas en el proyecto.

## Uso de la API

### Obtener token de autenticación

`POST /api/token/`

Body JSON:

```json
{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```

Obtendrás un `access` y `refresh` token para autenticarte.

---

### CRUD Direcciones

- Listar direcciones: `GET /api/addresses/`
- Crear dirección: `POST /api/addresses/`
- Actualizar dirección: `PUT /api/addresses/{id}/`
- Eliminar dirección: `DELETE /api/addresses/{id}/`

---

### CRUD Conductores

- Listar conductores: `GET /api/drivers/`
- Crear conductor: `POST /api/drivers/`
- Actualizar conductor: `PUT /api/drivers/{id}/`
- Eliminar conductor: `DELETE /api/drivers/{id}/`

---

### Solicitar servicio

`POST /api/services/request-service/`

Body JSON:

```json
{
  "client_address_id": 1
}
```

- Asigna el conductor más cercano disponible.
- Retorna detalles del servicio creado.

---

### Completar servicio

`POST /api/services/{id}/complete/`

Completa un servicio y vuelve disponible al conductor.

---

## Poblar datos falsos

Para generar direcciones y conductores falsos:

```bash
docker-compose exec web python manage.py populate_fake_data
```

Se generarán automáticamente 20 direcciones y 20 conductores.

---

## Flujo completo de prueba de la API

1. Authenticarse y obtener token.

Request:
```http request
POST /api/token/
Content-Type: application/json
```

Body JSON:

```json
{
  "username": "usuario",
  "password": "contraseña"
}
```
Respuesta exitosa:

```json
{
  "access": "access_token_aqui",
  "refresh": "refresh_token_aqui"
}
```
> Notas: Usa el access token para autenticar las siguientes peticiones.
> En cada request protegido, añade un header:
> Authorization: Bearer <access_token>

2. Listar Direcciones disponibles

Request:
```http request
GET /api/addresses/
Authorization: Bearer <access_token>
```
Respuesta exitosa:

```json
[
  {
    "id": 1,
    "street": "6671 Page Mountain Apt. 946",
    "city": "Port Stephanie",
    "latitude": -73.35,
    "longitude": -70.40
  },
  ...
]
```
> Elige una dirección (client_address_id) para solicitar un servicio.

3. Solicitar un Servicio

Request:
```http request
POST /api/services/request-service/
Authorization: Bearer <access_token>
Content-Type: application/json
```
Body JSON:

```json
{
  "client_address_id": 1
}
```
Respuesta exitosa:

```json
{
  "id": 1,
  "client_address": 1,
  "driver": 5,
  "status": "pending",
  "estimated_time_minutes": 8,
  "created_at": "2025-04-27T02:00:00Z"
}
```

> El sistema asignará automáticamente el conductor disponible más cercano.

4. Consultar Servicios

Request:
```http request
GET /api/services/
Authorization: Bearer <access_token>
```

Respuesta exitosa:

```json
[
  {
    "id": 1,
    "client_address": 1,
    "driver": 5,
    "status": "pending",
    "estimated_time_minutes": 8,
    "created_at": "2025-04-27T02:00:00Z"
  }
]
```
5. Marcar un Servicio como Completado

Cuando el servicio haya sido realizado, el conductor puede marcarlo como completed.

Request:
```http request
POST /api/services/1/complete/
Authorization: Bearer <access_token>
```

Respuesta exitosa:

```json
{
  "message": "Service marked as completed."
}
```
> El servicio pasa a estado completed y el conductor vuelve a estar disponible para nuevas asignaciones.

### Observaciones:
Los conductores son asignados de acuerdo a la distancia mínima al cliente (simple distancia Euclidiana).

Si no hay conductores disponibles, la API retorna un error manejado.

Cada servicio está protegido por autenticación JWT.

---

## Tests

Para correr los tests:

```bash
docker-compose exec web coverage run --rcfile=.coveragerc manage.py test
```

(Tests básicos cubren creación de servicios, asignación de conductores y flujo de finalización.)

Para ver el reporte de cobertura:

```bash
docker-compose exec web coverage report
```
```text
Name                       Stmts   Miss  Cover
----------------------------------------------
addresses/models.py            6      0   100%
addresses/serializers.py       6      0   100%
addresses/views.py             8      0   100%
drivers/models.py              6      0   100%
drivers/serializers.py         6      0   100%
drivers/views.py               8      0   100%
services/models.py            10      0   100%
services/serializers.py        7      0   100%
services/views.py             50      6    88%
----------------------------------------------
TOTAL                        107      6    94%

```
---

## Despliegue en Cloud (AWS / GCP)

### GCP

- **Servicio de backend:** Cloud Run o GKE para contenedores.
- **Base de datos:** Cloud SQL para PostgreSQL.
- **Almacenamiento estático:** Cloud Storage.
- **Seguridad:**
  - Variables sensibles mediante Secret Manager.
  - Comunicación HTTPS obligatoria.
  - IAM roles específicos para cada servicio.

Parte 1: Script básico para desplegar en Google Cloud Run

```bash
#!/bin/bash

# Variables
PROJECT_ID="tu-id-proyecto-gcp"
SERVICE_NAME="alfred-backend"
REGION="us-central1"

# Build imagen de Docker
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Desplegar en Cloud Run
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars DJANGO_SETTINGS_MODULE=alfred.settings \
    --port 8000
```

Este script hace lo siguiente:

1. Hace `docker build` usando Cloud Build.
2. Sube la imagen a Google Container Registry.
3. Despliega en Cloud Run.
4. Expone el servicio en puerto 8000.
5. Permite tráfico público (--allow-unauthenticated).

### ¿Por qué elegí Google Cloud Run en vez de AWS?

| Criterio | Google Cloud Run | AWS (Fargate / Elastic Beanstalk) |
|:---------|:-----------------|:---------------------------------|
| **Simplicidad de despliegue** | Muy sencillo: `gcloud run deploy` con configuración mínima. | Más pasos: definición de servicios ECS, creación de clusters, task definitions. |
| **Autoescalado a cero** | Nativo: escala de 0 a N instancias automáticamente. | En ECS o Fargate escalar a cero no es automático; requiere configuraciones especiales. |
| **Costo** | Pago exacto por invocación y tiempo de ejecución. Muy barato para proyectos que no tienen tráfico constante. | Fargate cobra por recursos reservados incluso si no hay tráfico. Elastic Beanstalk requiere instancias EC2 mínimas. |
| **HTTPS automático** | Gratis y habilitado por defecto en Cloud Run. | En AWS debes configurar un Load Balancer + ACM + Route53 para HTTPS. |
| **Configuración inicial** | Muy rápida: despliegue directo de imagen Docker. | AWS requiere configurar VPCs, subnets, security groups (más complejo). |
| **Ideal para pruebas técnicas y MVPs** | Sí, despliegues rápidos, sin infraestructura. | Más complejo y con más sobrecarga para proyectos pequeños o prototipos. |

> Nota: AWS tiene servicios excelentes, pero para este caso específico, la simplicidad y rapidez de Google Cloud Run lo hacen más atractivo.
---

## Notas

- El sistema calcula distancia usando fórmula simple (Euclidiana) para simplificación.
- No se implementó geocoding real ni navegación, dado el alcance de la prueba.
- Autenticación basada en JWT simple para proteger los endpoints.
- El servicio simula tiempos de llegada estimados.

