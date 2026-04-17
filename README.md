# 🚀 Vinculador DMAF

Sistema desarrollado para automatizar el análisis y vinculación entre proyectos y aliados estratégicos, permitiendo identificar oportunidades de cofinanciación de forma eficiente.

---

## 📌 Descripción

El **Vinculador DMAF** es una solución basada en servicios cloud (Azure) que permite:

- Cargar documentos de proyectos y aliados
- Procesar automáticamente la información
- Analizar compatibilidad entre proyectos y aliados
- Reducir significativamente el tiempo de evaluación

El sistema utiliza procesamiento asíncrono, inteligencia artificial y arquitectura serverless para lograr escalabilidad y eficiencia.

📖 Documento técnico: :contentReference[oaicite:0]{index=0}

---

## 🎯 Objetivos

### Generales
- Proveer una arquitectura escalable y eficiente para el análisis de proyectos.

### Específicos
- Automatizar el análisis de documentos
- Integrar servicios de IA para procesamiento de contenido
- Implementar una arquitectura basada en eventos
- Garantizar monitoreo y trazabilidad del sistema
- Definir estrategia de integración y despliegue continuo :contentReference[oaicite:1]{index=1}

---

## ⚙️ Funcionalidades

- 📂 Carga de documentos (proyectos y aliados)
- 📄 Visualización de documentos cargados
- ❌ Eliminación de documentos
- 🤖 Análisis automático de compatibilidad
- 📊 Procesamiento asíncrono de información
- 🔔 Sistema de notificaciones por correo

---

## 🏗️ Arquitectura

La solución está basada en una arquitectura cloud sobre **Microsoft Azure**, utilizando servicios PaaS y serverless.

### Componentes principales

- **Azure Web App**
  - Frontend / Backoffice
  - Gestión de iniciativas

- **Azure Functions**
  - API REST serverless
  - Gestión de documentos (carga, listado, eliminación)
  - Orquestación de procesos

- **Azure Blob Storage**
  - Almacenamiento de documentos
  - Archivos JSONL para procesamiento batch

- **Azure Cosmos DB**
  - Base de datos NoSQL
  - Gestión de estados de procesamiento asíncrono

- **Azure Data Factory**
  - Orquestación de pipelines
  - Integración con Databricks mediante triggers

- **Azure Databricks**
  - Procesamiento de datos
  - Integración con servicios de IA

- **Azure Document Intelligence**
  - Extracción de información estructurada desde documentos

- **Azure OpenAI**
  - Análisis de contenido en batch (procesos asincrónicos)

📌 El procesamiento en OpenAI se realiza en modo batch y puede tardar hasta 24 horas dependiendo del volumen de datos. :contentReference[oaicite:2]{index=2}

---

## 🔄 Flujo de procesamiento

1. Usuario carga documentos
2. Se almacenan en Blob Storage
3. Se dispara un evento (trigger)
4. Data Factory ejecuta pipeline
5. Databricks procesa la información
6. Se envía análisis a OpenAI (batch)
7. Se actualiza el estado en Cosmos DB
8. Se notifican resultados al usuario

---

## 🔔 Sistema de Notificaciones

Incluye arquitectura transversal para envío de correos:

- Azure Functions (gestión de envío)
- Azure Communication Services (email)
- Blob Storage (plantillas)
- Cosmos DB (configuración de notificaciones)

Permite gestionar destinatarios, plantillas y parámetros dinámicos por iniciativa. :contentReference[oaicite:3]{index=3}

---

## 📊 Monitoreo y Logs

El sistema utiliza herramientas nativas de Azure:

- Application Insights
- Logs en Azure Web App
- Logs de Azure Functions
- Monitoreo de pipelines en Data Factory
- Logs de ejecución en Databricks

---

## 🧪 Ambientes

Actualmente el sistema cuenta con:

- 1 ambiente configurado (según disponibilidad del cliente) :contentReference[oaicite:4]{index=4}

---

## 🛠️ Tecnologías

- Azure Web Apps
- Azure Functions (Serverless)
- Azure Blob Storage
- Azure Cosmos DB
- Azure Data Factory
- Azure Databricks
- Azure OpenAI
- Azure Document Intelligence

---

## 🚀 Despliegue

El código fuente se encuentra gestionado en:

- Azure DevOps (repositorio del cliente) :contentReference[oaicite:5]{index=5}

---

## 🔐 Seguridad

- Control de acceso basado en servicios Azure
- Gestión de datos en servicios seguros (Cosmos DB, Blob Storage)
- Procesamiento controlado mediante pipelines y servicios serverless

---

## 🧾 Auditoría

El sistema incluye un servicio transversal de auditoría:

- API dedicada en Azure Functions
- Registro centralizado en Cosmos DB
- Integración con diferentes componentes del ecosistema

---

## 👥 Equipo

- Data Science
- Full Stack Developers
- Technical Leader
- Project Analyst

---

## 📬 Contacto

Proyecto desarrollado para:

**CAF (Banco de Desarrollo de América Latina)**

---

## 📎 Notas

- Arquitectura basada en eventos (event-driven)
- Procesamiento asíncrono
- Escalable y orientado a microservicios
- Uso de procesamiento batch para análisis con IA

---
