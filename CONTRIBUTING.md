# 🤝 Guía de Contribución – Vinculador DMAF

Gracias por tu interés en contribuir al proyecto **Vinculador DMAF**.

Este repositorio es de uso corporativo, por lo que las contribuciones deben seguir los lineamientos descritos a continuación.

---

## 📌 Alcance del repositorio

- Aplicación web (Backoffice) desplegada en Azure Web App
- APIs serverless desarrolladas en Azure Functions
- Procesamiento de documentos mediante Azure Databricks
- Integración con Azure OpenAI y Document Intelligence
- Orquestación de procesos con Azure Data Factory
- Almacenamiento en Blob Storage y Cosmos DB
- Sistema de notificaciones y auditoría

---

## 🛠️ Flujo de trabajo

1. Crear una rama desde `main` o `development`:
   git checkout -b feature/nombre-funcionalidad

2. Mantener cambios pequeños, claros y enfocados

3. Probar localmente:
   - Azure Functions
   - Integraciones (si aplica)
   - Validación de endpoints

4. Crear Pull Request incluyendo:
   - Descripción clara del cambio
   - Justificación técnica / funcional
   - Impacto esperado
   - Evidencia (logs, screenshots, pruebas)

---

## 📐 Convenciones de código

### Backend (Azure Functions)

- Funciones desacopladas y reutilizables
- Uso de buenas prácticas REST
- Manejo adecuado de errores
- Logging estructurado

---

### Databricks / Procesamiento

- Paradigma funcional
- Funciones separadas por responsabilidad
- Evitar lógica monolítica
- Uso eficiente de recursos

---

### Frontend (Web App)

- Código limpio y modular
- Manejo claro de eventos
- Separación de responsabilidades (UI / lógica)

---

### General

- Nombres descriptivos (variables, funciones, endpoints)
- Evitar hardcodeo de valores
- Uso de variables de entorno
- Código documentado cuando sea necesario

---

## 🔐 Seguridad

- ❌ No subir secretos, tokens o credenciales
- ❌ No exponer endpoints internos
- ❌ No hardcodear claves en el código

- ✅ Usar variables de entorno
- ✅ Usar Managed Identity cuando aplique
- ✅ Validar inputs en APIs
- ✅ Manejo seguro de datos sensibles

---

## 📋 Checklist antes del PR

- [ ] El código compila / ejecuta sin errores
- [ ] APIs responden correctamente
- [ ] No rompe flujos existentes
- [ ] No afecta pipelines (Data Factory / Databricks)
- [ ] No introduce dependencias innecesarias
- [ ] Variables de entorno correctamente definidas
- [ ] Logs y manejo de errores implementados
- [ ] Documentación actualizada (si aplica)

---

## 🔄 Estrategia de ramas

- main → Producción
- development → Integración
- feature/* → Nuevas funcionalidades
- hotfix/* → Correcciones urgentes

---

## 🚀 Buenas prácticas

- Mantener PRs pequeños
- Evitar cambios masivos sin revisión
- Validar impacto en procesamiento batch (OpenAI)
- Probar integraciones end-to-end cuando aplique

---

## 📞 Contacto

Proyecto mantenido por el equipo Vinculador DMAF – CAF

Para cambios estructurales o de arquitectura, coordinar previamente con:

- Technical Leader
- Arquitecto de la solución
- Equipo de Data / AI
