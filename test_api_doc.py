from fastapi.testclient import TestClient
import api

c = TestClient(api.app)
# 1. buscar
b = c.get("/buscar", params={"consulta": '"contrato estatal"', "pagina": 0}).json()
r0 = b["resultados"][0]
print("Buscar OK | radicado:", r0["radicado"], "| paginas:", b["total_paginas"])

# 2. obtener texto del primer resultado
d = c.get("/documento", params={"url_documento": r0["url_documento"]})
print("Documento HTTP:", d.status_code)
j = d.json()
print("PDF paginas:", j.get("paginas"), "| chars:", len(j.get("texto") or ""))
print("url_pdf:", (j.get("url_pdf") or "")[:70])
print("\n--- primeros 300 chars ---")
print((j.get("texto") or "")[:300])
