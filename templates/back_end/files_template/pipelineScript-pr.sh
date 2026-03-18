# ═══════════════════════════════════════════════════════════════════════════════
# pipelineScript-pr
# ═══════════════════════════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────────────────────────────
# Creación estructura de direcctorios para artefactos build/deploy
# ───────────────────────────────────────────────────────────────────────────────
echo "Creando directorios de artefactos: artifact/deploy"
mkdir -p artifact/deploy

# ───────────────────────────────────────────────────────────────────────────────
# Dockerfile en el directorio raíz (donde está el contexto de build)
# ───────────────────────────────────────────────────────────────────────────────
echo "Copiando Dockerfile al directorio raíz para el contexto de build"
cp manifest/feature/Dockerfile ./

# ───────────────────────────────────────────────────────────────────────────────
# Archivos para pruebas/deploy dentro de los artefactos
# ───────────────────────────────────────────────────────────────────────────────
echo "Copiando archivos de pruebas a los artefactos"
mkdir -p artifact/deploy/ingresstransversal
cp -r tests artifact/deploy/

# ───────────────────────────────────────────────────────────────────────────────
# Quitamos instalación en host para evitar incompatibilidad
# ───────────────────────────────────────────────────────────────────────────────
# pip install -r requirements.txt
echo "Skipping pip install on host. Dependencies will be installed inside Docker container."
