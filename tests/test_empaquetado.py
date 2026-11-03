"""Pruebas de empaquetar.py: el ZIP de entrega no debe incluir archivos internos
del asistente de IA (CLAUDE.md, .claude/), credenciales (.env, secrets.toml) ni
entornos o cachés, aunque aparezcan dentro de carpetas que sí se entregan."""

import os
import shutil
import tempfile
import unittest
import zipfile
from unittest import mock

import empaquetar


class TestEmpaquetado(unittest.TestCase):

    def setUp(self):
        # Copia mínima del proyecto en una carpeta temporal, con archivos "trampa".
        self.raiz = tempfile.mkdtemp()
        for carpeta in ("docs", "casos_prueba", "algebra/.claude", "tests/__pycache__"):
            os.makedirs(os.path.join(self.raiz, carpeta), exist_ok=True)
        archivos = {
            "app.py": "", "README.md": "", "requirements.txt": "", "ejecutar.bat": "",
            "docs/manual_usuario.md": "", "docs/herramientas_y_bibliotecas.md": "uso de IA",
            "casos_prueba/README.md": "", "algebra/matriz.py": "",
            # trampas
            "CLAUDE.md": "x", "docs/CLAUDE.md": "x", "algebra/.claude/settings.json": "{}",
            "algebra/.env": "TOKEN=1", "docs/.env.local": "x", ".streamlit/secrets.toml": "x",
            "tests/__pycache__/a.pyc": "",
        }
        os.makedirs(os.path.join(self.raiz, ".streamlit"), exist_ok=True)
        for relativo, contenido in archivos.items():
            with open(os.path.join(self.raiz, relativo), "w", encoding="utf-8") as f:
                f.write(contenido)

    def tearDown(self):
        shutil.rmtree(self.raiz, ignore_errors=True)

    def test_no_incluye_archivos_internos_ni_credenciales(self):
        with mock.patch.object(empaquetar, "RAIZ", self.raiz):
            incluidos = {r.replace(os.sep, "/") for r in empaquetar.archivos_a_incluir()}
        for prohibido in ("CLAUDE.md", "docs/CLAUDE.md", "algebra/.claude/settings.json",
                          "algebra/.env", "docs/.env.local", ".streamlit/secrets.toml",
                          "tests/__pycache__/a.pyc"):
            self.assertNotIn(prohibido, incluidos)
        # La declaración de herramientas (uso de IA) sí se entrega.
        self.assertIn("docs/herramientas_y_bibliotecas.md", incluidos)
        self.assertIn("algebra/matriz.py", incluidos)

    def test_zip_generado_con_una_sola_raiz(self):
        with mock.patch.object(empaquetar, "RAIZ", self.raiz), \
                mock.patch("sys.argv", ["empaquetar.py", "01"]):
            self.assertEqual(empaquetar.main(), 0)
        ruta = os.path.join(self.raiz, "dist", "Grupo01-IF0012-Proyecto-IIC.zip")
        with zipfile.ZipFile(ruta) as zf:
            nombres = zf.namelist()
        self.assertEqual({n.split("/")[0] for n in nombres}, {"Grupo01-IF0012-Proyecto-IIC"})
        self.assertFalse(any("claude" in n.lower() or ".env" in n for n in nombres))


class TestGitignore(unittest.TestCase):
    """El repositorio de GitHub no debe poder rastrear credenciales por accidente."""

    def test_excluye_credenciales_y_archivos_internos(self):
        ruta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".gitignore")
        with open(ruta, encoding="utf-8") as f:
            reglas = {linea.strip() for linea in f if linea.strip() and not linea.startswith("#")}
        for regla in (".env", ".env.*", "*.pem", "*.key", ".streamlit/secrets.toml",
                      "CLAUDE.md", ".claude/", ".venv/", "__pycache__/"):
            self.assertIn(regla, reglas)


if __name__ == "__main__":
    unittest.main()
