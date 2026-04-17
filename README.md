# 🚀 Vinculador DMAF

![Azure](https://img.shields.io/badge/Azure-Cloud-blue)
![Architecture](https://img.shields.io/badge/Architecture-Event--Driven-orange)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-Private-red)

Sistema desarrollado para automatizar el análisis y vinculación entre proyectos y aliados estratégicos, permitiendo identificar oportunidades de cofinanciación de forma eficiente.

---

## 📌 Descripción

El **Vinculador DMAF** es una solución basada en servicios cloud (Azure) que permite:

- Cargar documentos de proyectos y aliados
- Procesar automáticamente la información
- Analizar compatibilidad entre proyectos y aliados
- Reducir significativamente el tiempo de evaluación

El sistema utiliza procesamiento asíncrono, inteligencia artificial y arquitectura serverless para lograr escalabilidad y eficiencia.

---

## 🎯 Objetivos

### Generales
- Proveer una arquitectura escalable y eficiente para el análisis de proyectos.

### Específicos
- Automatizar el análisis de documentos
- Integrar servicios de IA para procesamiento de contenido
- Implementar una arquitectura basada en eventos
- Garantizar monitoreo y trazabilidad del sistema
- Definir estrategia de integración y despliegue continuo

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

### 📊 Diagrama de arquitectura

Agregar imagen en `/docs/architecture.png`

---

### 🧩 Componentes principales

- Azure Web App
- Azure Functions
- Azure Blob Storage
- Azure Cosmos DB
- Azure Data Factory
- Azure Databricks
- Azure Document Intelligence
- Azure OpenAI

---

## 🔄 Flujo de procesamiento

Usuario → Upload → Blob Storage → Trigger → Data Factory → Databricks → OpenAI → Cosmos DB → Notificación

---

## 🔔 Sistema de Notificaciones

- Azure Functions
- Azure Communication Services
- Blob Storage
- Cosmos DB

---

## 📊 Monitoreo y Logs

- Application Insights
- Logs Azure Functions
- Data Factory Monitoring
- Databricks logs

---

## 🛠️ Tecnologías

Azure, Databricks, OpenAI, Cosmos DB, Blob Storage

---

## 🚀 Getting Started

```bash
git clone <repo-url>
cd vinculador-dmaf
```

---

## 📁 Estructura

```
.
├── src/
├── functions/
├── pipelines/
├── notebooks/
├── docs/
└── README.md
```

---

## 📬 Contacto

CAF (Banco de Desarrollo de América Latina)
