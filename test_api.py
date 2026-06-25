from fastapi.testclient import TestClient
import api

c = TestClient(api.app)
r = c.get("/buscar", params={"consulta": '"contrato estatal"', "pagina": 0})
print("HTTP", r.status_code)
d = r.json()
print("total_paginas:", d["total_paginas"], "| en pagina:", d["resultados_en_pagina"])
r0 = d["resultados"][0]
print("primer radicado:", r0["radicado"], "| interno:", r0["interno"])
print("ponente:", r0["ponente"])
print("doc:", (r0["url_documento"] or "")[:70])
print("health:", c.get("/").json())
