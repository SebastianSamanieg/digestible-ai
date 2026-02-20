# Configuración Inicial del Proyecto

Este documento detalla los pasos necesarios para configurar el entorno de desarrollo desde cero.

---

## 1. Requisito: Versión de Python
Este proyecto requiere **Python 3.12.10**. 

## 2. Creación del Entorno Virtual (venv)
Para aislar las librerías del proyecto, crea un entorno virtual ejecutando:
```bash
py -3.12 -m venv venv
```

## 3. Activación del Entorno Virtual
Activa el entorno según tu sistema operativo:

**Windows (PowerShell o CMD):**
```bash
.\venv\Scripts\activate
```
> **Tip:** Una vez activo, verás `(venv)` al inicio de tu terminal.

## 4. Configuración de Variables de Entorno
Crea tu archivo `.env` a partir de la plantilla proporcionada:

**Windows (PowerShell o CMD):**
```bash
copy .env.example .env
```
Luego, edita el archivo `.env` con tus credenciales:
- Configura `LOG_LEVEL` (TRACE/DEBUG/INFO/WARNING/ERROR)
- Elige tu `LLM_PROVIDER` (OPENAI/GOOGLE)
- Completa las claves API según el proveedor que uses

## 5. Instalación de Dependencias
Con el entorno virtual activado, instala los requerimientos del proyecto:
```bash
python.exe -m pip install --upgrade pip 
pip install -r requirements.txt
```

---