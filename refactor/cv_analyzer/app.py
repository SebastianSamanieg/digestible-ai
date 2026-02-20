import streamlit as st
import sys
from pathlib import Path

# Obtener el path absoluto y subir un nivel
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

print(f"Project root: {project_root}")  # Para debug
print(f"sys.path: {sys.path[:3]}")  # Para debug

from cv_analyzer.ui.streamlit_ui import main

if __name__ == "__main__":
    main()