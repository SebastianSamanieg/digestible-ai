# 🚀 Configuración Inicial del Proyecto

Bienvenido 👋  
Sigue estos pasos para configurar el entorno de desarrollo correctamente desde cero.

---

# 🐍 1. Requisito: Versión de Python

Este proyecto requiere:

> **Python 3.13.12 (Feb. 3, 2026)**

## ✅ Verifica tu versión instalada

```bash
py -3.13 --version
```

Si no tienes la versión correcta, descárgala aquí (Windows 64-bit):

https://www.python.org/ftp/python/3.13.12/python-3.13.12-amd64.exe

---

# 📦 2. Crear el Entorno Virtual (venv)

Para aislar las dependencias del proyecto y evitar conflictos:

```bash
py -3.13 -m venv venv
```

Esto creará una carpeta llamada `venv` dentro del proyecto.

---

# ⚡ 3. Activar el Entorno Virtual

## 🪟 Windows (PowerShell o CMD)

```bash
.\venv\Scripts\activate
```

## ✅ Confirmación

Si todo está correcto, verás algo como:

```bash
(venv) C:\ruta\del\proyecto>
```

---

# 📥 4. Instalar Dependencias

Con el entorno virtual activado:

## 🔄 Actualiza pip

```bash
python -m pip install --upgrade pip
```

## 📚 Instala los requerimientos del proyecto

```bash
pip install -r requirements.txt
```

---

# 🔐 5. Configuración de Variables de Entorno

## 📄 Crear archivo `.env`

```bash
copy .envexample .env
```

## ✏️ Editar el archivo `.env`

Configura:

- `LOG_LEVEL` → TRACE | DEBUG | INFO | WARNING | ERROR  
- Las keys del secreto → `secret-koral-ia`

---

# 🧠 Buenas Prácticas

- 1 Proyecto = 1 venv  
- Nunca instalar dependencias en el Python global  
- Siempre activar el entorno antes de trabajar  

---

# 🧩 Estructura Esperada del Proyecto

```bash
digestible-ai/
│
├── venv/
├── .env
├── requirements.txt
└── src/
```