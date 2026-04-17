# 📘 Guía de Despliegue – Vinculador DMAF

## 📑 Tabla de contenidos
- [Introducción](#-introducción)
- [Requisitos Previos](#-requisitos-previos)
- [Arquitectura Técnica](#-arquitectura-técnica)
- [Procedimiento de Despliegue](#-procedimiento-de-despliegue)
- [Validaciones Post-Despliegue](#-validaciones-post-despliegue)
- [Seguridad y Buenas Prácticas](#-seguridad-y-buenas-prácticas)
- [Nomenclatura Estándar](#-nomenclatura-estándar)
- [Rollback y Recuperación](#-rollback-y-recuperación)

---

## 🧭 Introducción

Esta guía describe el procedimiento técnico para desplegar en producción la solución **VINCULADOR DMAF** en Microsoft Azure.

La solución integra:
- Servicios de inteligencia artificial (Azure OpenAI)
- Arquitectura serverless
- Almacenamiento estructurado
- Procesamiento de datos mediante pipelines

Su objetivo es optimizar la gestión y análisis de documentos dentro del CAF. :contentReference[oaicite:0]{index=0}

---

## 🧱 Requisitos Previos

### ✔ Grupos de recursos

Se deben considerar los siguientes:

- `RG-POC-VINCULADOR-CR`
- `RG-POC-iDataFactory-CR`

Se recomienda contar con ambientes separados:
- Desarrollo (POC)
- Producción :contentReference[oaicite:1]{index=1}

---

### ✔ Control de acceso (IAM)

Asignar rol:

- **Colaborador (Contributor)** a usuarios del proyecto
- **Key Vault Administrator** al grupo:
  - `GS_AZ_INFRA_ADM`

---

### ✔ Azure DevOps

Proyecto: `Innovation Lab`

Repositorios:

- caf-frontend
- caf-vinculador-api
- caf-auditoria-api
- caf-notication-api
- caf-userpermissions-api
- caf-common
- caf-vinculador-model :contentReference[oaicite:2]{index=2}

---

### ✔ Permisos requeridos

Suscripción Azure con acceso a:

- App Services
- Azure Functions
- Cosmos DB
- Azure OpenAI
- Document Intelligence
- Storage Account
- Data Factory
- Databricks
- Communication Services

---

## 🏗 Arquitectura Técnica

### Servicios principales

- **App Service**
  - Frontend de la solución
  - Dominio: `app-idatafactory-cr.azurewebsites.net`

- **Azure Functions**
  - Backend serverless (APIs)

- **Cosmos DB**
  - Almacenamiento de logs y auditoría

- **Azure Storage**
  - Almacenamiento de documentos y datos procesados

- **Azure OpenAI**
  - Procesamiento de lenguaje natural

- **Azure Document Intelligence**
  - Extracción de texto (OCR)

- **Azure Data Factory**
  - Orquestación de pipelines

- **Azure Databricks**
  - Procesamiento de datos e integración con IA

📌 Arquitectura basada en integración de servicios y procesamiento asíncrono. :contentReference[oaicite:3]{index=3}

---

## 🚀 Procedimiento de Despliegue

### 🔹 Fase 1: Creación de ambientes

Se recomienda:

- Ambiente Desarrollo (POC)
- Ambiente Producción

Cada ambiente debe tener:

- Grupo de recursos independiente
- Configuración de seguridad
- Escalabilidad adecuada

---

### 🔹 Fase 2: Configuración en Azure DevOps

#### ✔ Service Principal

Crear uno por ambiente:

- DEV
- Producción

Permisos:

- Contributor
- User Access Administrator

---

#### ✔ Service Connections

- Dev: `dev-caf-service-connection`
- Producción: service connection independiente

---

#### ✔ Manejo de ramas

- `development`
- `main`

---

#### ✔ Variables de entorno

Crear grupos de variables por ambiente:

- Configuración de servicios
- Endpoints
- Credenciales

---

#### ✔ Pipelines

Crear pipelines por ambiente:

- Build
- Deploy

Ejecutar pipelines para desplegar:

- Azure Functions
- Web App

---

## 🔄 Despliegue de Recursos

### ✔ App Service (Frontend)

- Exportar plantilla ARM desde entorno DEV
- Importar en Producción
- Ajustar:
  - Nombre
  - Plan (mínimo **Premium v3 P1V3**)
  - Variables de entorno
- Ejecutar pipeline `caf-frontend`

---

### ✔ Azure Functions (Backend)

Incluye:

- API principal
- Permisos
- Commons
- Notificaciones
- Auditoría

Pasos:

- Exportar ARM
- Importar en Producción
- Configurar variables
- Ejecutar pipelines correspondientes

---

### ✔ Cosmos DB

- Exportar configuración
- Crear base de datos en Producción
- Configurar:
  - Contenedores
  - Particiones
  - Claves de acceso

---

### ✔ Azure Storage

- Crear recurso en Producción
- Configurar:
  - Contenedores
  - Accesos
- Migrar datos si es necesario

---

### ✔ Azure OpenAI

Configurar manualmente:

- Modelo (ej: GPT-4o)
- Región
- Límites de consumo

---

### ✔ Azure Document Intelligence

- Crear recurso en Producción
- Importar o reentrenar modelos si aplica

---

### ✔ Azure Data Factory

- Exportar pipeline
- Configurar:
  - Variables
  - Conexión con Databricks
  - Pipeline `VINCULADOR_DMAF`

---

### ✔ Azure Databricks

- Configurar credenciales Git
- Clonar repositorio
- Configurar notebooks
- Validar conexión con Data Factory

---

## 🔍 Validaciones Post-Despliegue

- Validar acceso a Web App
- Verificar ejecución de APIs
- Confirmar carga de documentos en Blob Storage
- Validar ejecución de pipelines
- Confirmar procesamiento en Databricks
- Verificar resultados en Cosmos DB

---

## 🔐 Seguridad y Buenas Prácticas

- Uso de **Managed Identity**
- Control de acceso mediante **RBAC**
- Gestión de secretos en **Key Vault**
- Separación de ambientes
- Uso de HTTPS/TLS

---

## 🏷 Nomenclatura Estándar

Formato:
