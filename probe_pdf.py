"""Prueba la API publica de descarga de SAMAI y extrae texto del PDF."""
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}
corp = "1100103"
radicado = "13001233300020190036201"
hash_cert = "C490A4E3BBE5ADD79FF1EF3CC780F74448533EE6B6A3BEE5D8B5DB2E1968F808"

for sufijo in ("2", "1", "0"):
    url = (f"https://samaicore.consejodeestado.gov.co/api/"
           f"DescargarProvidenciaPublica/{corp}/{radicado}/{hash_cert}/{sufijo}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=60)
        ct = r.headers.get("Content-Type", "")
        print(f"[/{sufijo}] STATUS {r.status_code} | {ct} | {len(r.content)} bytes")
        if r.status_code == 200 and ("pdf" in ct or r.content[:4] == b"%PDF"):
            fn = f"providencia_{sufijo}.pdf"
            with open(fn, "wb") as f:
                f.write(r.content)
            print(f"     >> PDF guardado: {fn}")
            break
    except Exception as e:
        print(f"[/{sufijo}] ERROR {e}")
