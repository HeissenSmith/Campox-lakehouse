# 🚀 Proyecto Lakehouse – Campox

Implementación de una arquitectura **Lakehouse** moderna sobre **Google Cloud Platform (GCP)**  
para la empresa *Campox*, orientada a integrar, procesar y analizar datos operacionales.

---

## 🧩 Arquitectura General

La solución está construida bajo un enfoque **event-driven y desacoplado**, integrando servicios nativos de GCP:

| Componente | Descripción |
|-------------|-------------|
| ☁️ **Cloud SQL (MySQL – csantoyo)** | Base transaccional de origen con tablas normalizadas. |
| 🗂️ **Cloud Storage (DataEntry)** | Almacena archivos planos subidos manualmente (ej. `orderdetails.csv`). |
| ⚙️ **Cloud Functions (EventDriver)** | Detecta la carga de archivos y dispara la ingesta automática. |
| 🕒 **Cloud Scheduler + Cloud Run** | Orquesta la ejecución programada de flujos ETL desde Cloud SQL. |
| 🧮 **BigQuery (RAW + STAGING)** | Aloja las tablas federadas y el modelo desnormalizado optimizado para analítica. |
| 📊 **Looker Studio / Power BI** | Capa de visualización de KPIs y reportes comerciales. |

---

## 🧠 Objetivos del Proyecto

- Automatizar la **ingesta** de datos desde MySQL y archivos planos.  
- Implementar una **arquitectura escalable y trazable** con GCP.  
- Desarrollar un **modelo desnormalizado** en BigQuery para análisis OLAP.  
- Crear dashboards interactivos para análisis comercial y operativo.  

---

## 🗂️ Estructura del Repositorio

