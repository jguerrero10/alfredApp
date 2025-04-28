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
