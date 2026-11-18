
"""Cliente RESTCONF para Cisco IOS-XE."""
# Autor: JAIRO ROSAS ENRIQUEZ
# U4ACT04 - DevOps con RESTCONF

import os

import requests
import urllib3


HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}


class RestconfClient:
    def __init__(self, host, port=443):
        self.base = f"https://{host}:{port}/restconf/data"

        # Credenciales mediante variables de entorno
        self.auth = (
            os.environ["SANDBOX_USER"],
            os.environ["SANDBOX_PASS"],
        )

        # Certificado autofirmado del Sandbox
        self.verify = (
            os.getenv("VERIFY_SSL", "false").lower() == "true"
        )

        if not self.verify:
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning
            )

    def _url(self, path):
        return f"{self.base}/{path}"

    def get(self, path):
        """Consulta la configuracion mediante RESTCONF."""
        r = requests.get(
            self._url(path),
            headers=HEADERS,
            auth=self.auth,
            verify=self.verify,
            timeout=30,
        )

        # Recursos sin contenido o inexistentes
        if r.status_code in (204, 404):
            return None

        r.raise_for_status()
        return r.json() if r.text else None

    def put(self, path, payload):
        """Crea o actualiza recursos mediante RESTCONF."""
        r = requests.put(
            self._url(path),
            headers=HEADERS,
            auth=self.auth,
            json=payload,
            verify=self.verify,
            timeout=30,
        )

        r.raise_for_status()

        # 201 = creado, 204 = actualizado
        return r.status_code
