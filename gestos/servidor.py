"""Canal local entre Python y la gráfica: solo viajan los 9 números de la cámara.

Por qué existe: medido en Brave (10-nov), una actualización por rerun de Streamlit llega
al navegador ~1 a 3 veces por segundo, porque Streamlit agrupa los reruns.  Con este
canal la cámara llega a ~30 veces por segundo sin rerun.  Ver docs/portabilidad_java_python.md.

- Escucha solo en 127.0.0.1 (no es accesible desde la red), en un puerto libre.
- GET  /camara?t=<token>   flujo Server-Sent Events con la cámara cada vez que cambia.
- POST /raton?t=<token>    el navegador avisa la cámara que dejó el ratón (para continuar
                           desde ahí sin saltos).
- El token aleatorio evita que otra página local lea o cambie el estado.
"""

import json
import secrets
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


class ServidorCamara:
    def __init__(self, al_mover_raton=None):
        self.token = secrets.token_urlsafe(16)
        self._camara = None
        self._version = 0
        self._cond = threading.Condition()
        self._activo = True
        self._al_mover_raton = al_mover_raton
        servidor = self

        class Manejador(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def _autorizado(self):
                consulta = parse_qs(urlparse(self.path).query)
                return secrets.compare_digest(consulta.get("t", [""])[0], servidor.token)

            def _cabeceras(self, codigo, tipo="text/plain"):
                self.send_response(codigo)
                self.send_header("Content-Type", tipo)
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

            def do_GET(self):
                if urlparse(self.path).path != "/camara" or not self._autorizado():
                    self._cabeceras(403)
                    return
                self._cabeceras(200, "text/event-stream")
                visto = -1
                try:
                    while servidor._activo:
                        with servidor._cond:
                            servidor._cond.wait_for(lambda: servidor._version != visto or not servidor._activo,
                                                    timeout=15)
                            version, camara = servidor._version, servidor._camara
                        if not servidor._activo:
                            break
                        if version == visto or camara is None:
                            self.wfile.write(b": latido\n\n")      # mantiene viva la conexión
                        else:
                            visto = version
                            self.wfile.write(f"data: {json.dumps(camara)}\n\n".encode())
                        self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    pass

            def do_POST(self):
                if urlparse(self.path).path != "/raton" or not self._autorizado():
                    self._cabeceras(403)
                    return
                try:
                    largo = min(int(self.headers.get("Content-Length", 0)), 2000)
                    camara = json.loads(self.rfile.read(largo))
                except (ValueError, json.JSONDecodeError):
                    self._cabeceras(400)
                    return
                if servidor._al_mover_raton:
                    servidor._al_mover_raton(camara)
                self._cabeceras(204)

            def do_OPTIONS(self):
                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

        self._http = ThreadingHTTPServer(("127.0.0.1", 0), Manejador)
        self._http.daemon_threads = True
        self.puerto = self._http.server_address[1]
        self._hilo = threading.Thread(target=self._http.serve_forever, name="gestos-servidor", daemon=True)
        self._hilo.start()

    def publicar(self, camara):
        with self._cond:
            self._camara = camara
            self._version += 1
            self._cond.notify_all()

    def cerrar(self):
        with self._cond:
            self._activo = False
            self._cond.notify_all()
        self._http.shutdown()
        self._http.server_close()
