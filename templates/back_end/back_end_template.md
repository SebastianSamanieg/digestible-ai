# 📁 Project Structure Template

> Basado en arquitectura **Clean Architecture / DDD** con FastAPI.  
> Reemplaza `<project-name>` con el nombre de tu proyecto.

---

## 🗂️ Árbol de Carpetas

```
<project-name>/
│
├── api/                            # Capa de presentación (rutas HTTP)
│   ├── routes/                     # Endpoints organizados por dominio
│   │   └── __init__.py
│   ├── schemas/                    # Modelos de entrada/salida
│   │   ├── request/
│   │   │   └── __init__.py
│   │   └── response/
│   │       ├── base_response.py    # Respuesta base genérica
│   │       └── __init__.py
│   └── __init__.py
│
├── config/                         # Configuración global de la app
│   ├── logger_config.py            # Setup del logger
│   └── __init__.py
│
├── core/                           # Núcleo de la aplicación
│   │
│   ├── domain/                     # Lógica de negocio pura
│   │   └── __init__.py
│   │
│   ├── infrastructure/             # Adaptadores hacia el exterior
│   │   ├── data_sources/           # Conexiones a bases de datos
│   │   │   ├── <db_type>_ds/       # Ej: sql_ds, redis_ds, mongo_ds
│   │   │   │   ├── repositories/   # Implementación del acceso a datos
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── connection.py   # Configuración de la conexión
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── services/               # Clientes de servicios externos (LLM, APIs)
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── workers/                    # Tareas en background / async jobs
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── manifest/                       # Kubernetes / Docker configs
│   ├── feature/
│   │   ├── deployment.yml
│   │   ├── Dockerfile
│   │   └── test-ingress-service.yml
│   └── trunk/
│       ├── deployment.yml
│       ├── Dockerfile
│       └── ingress-service.yml
│
├── utils/                          # Utilidades generales (helpers, decorators)
│   └── __init__.py
│
├── app.py                          # Configuración de la app FastAPI
├── main.py                         # Punto de entrada
├── requirements.txt                # Dependencias Python
├── venv/                           # Entorno virtual (NO commitear)
├── .env                            # Variables de entorno (NO commitear)
├── .envexample                     # Ejemplo de variables de entorno
├── .gitignore
├── README.md
├── sonar-project.properties        # Configuración SonarQube
├── pipelineParams.json             # Parámetros del pipeline CI/CD
├── pipelineScript.sh               # Script pipeline principal
└── pipelineScript-pr.sh            # Script pipeline para PRs
```

---
## 📌 Convenciones de Nomenclatura

|Tipo|Convención|Ejemplo|
|---|---|---|
|Carpetas|`snake_case`|`data_sources/`|
|Archivos Python|`snake_case.py`|`manager_factura.py`|
|Clases|`PascalCase`|`PromptProvider`|
|Archivos de config|`snake_case` o `kebab-case`|`llm_config.py`, `sonar-project.properties`|
|Archivos K8s/Docker|`kebab-case.yml`|`deployment.yml`|

---
