"""Valida la cadena completa: busqueda -> url_documento -> blob PDF -> texto."""
import io, re, requests, samai
from bs4 import BeautifulSoup
from pypdf import PdfReader

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

# 1. buscar -> token fresco
data = samai.buscar('"contrato estatal"', pagina=0)
r0 = data["resultados"][0]
print("Radicado:", r0["radicado"], "| Tipo:", r0["tipo_providencia"])

# 2. abrir el visor para sacar la URL del blob Azure
vp = requests.get(r0["url_documento"], headers=HEADERS, timeout=60)
soup = BeautifulSoup(vp.text, "html.parser")
btn = soup.find(id=re.compile(r"DescargarProvideciaLinkButton$"))
blob = btn["href"] if btn and btn.has_attr("href") else None
print("Blob URL:", (blob or "NO ENCONTRADA")[:90], "...")

# 3. descargar PDF y extraer texto
def get_con_reintentos(url, intentos=4):
    import time
    for n in range(intentos):
        try:
            return requests.get(url, headers=HEADERS, timeout=90)
        except requests.exceptions.ConnectionError as e:
            print(f"   reintento {n+1} (DNS/conexion)...")
            time.sleep(2)
    raise RuntimeError("fallo tras reintentos")

if blob:
    pdf = get_con_reintentos(blob)
    print("PDF status:", pdf.status_code, "| bytes:", len(pdf.content),
          "| es PDF:", pdf.content[:4] == b"%PDF")
    reader = PdfReader(io.BytesIO(pdf.content))
    texto = "\n".join((p.extract_text() or "") for p in reader.pages)
    print("Paginas PDF:", len(reader.pages), "| caracteres texto:", len(texto))
    print("\n----- PRIMEROS 600 CARACTERES -----")
    print(texto[:600])
