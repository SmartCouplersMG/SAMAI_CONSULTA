from fastapi.testclient import TestClient
import api

c = TestClient(api.app)
q = '"falla del servicio" AND "error judicial"'
a = c.get("/buscar", params={"consulta": q, "modo": "all"}).json()
b = c.get("/buscar", params={"consulta": q, "modo": "any"}).json()
print("modo=all (AND) paginas:", a["total_paginas"], "| en_pagina:", a["resultados_en_pagina"])
print("modo=any (OR)  paginas:", b["total_paginas"], "| en_pagina:", b["resultados_en_pagina"])
