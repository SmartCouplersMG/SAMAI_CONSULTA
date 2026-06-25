"""Sondeo: que devuelve VerProvidencia.aspx?tokenDocumento=JWT
Tomamos un token fresco de una busqueda real y analizamos la respuesta."""
import samai, requests

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

data = samai.buscar('"contrato estatal"', pagina=0)
r0 = data["resultados"][0]
url = r0["url_documento"]
print("Radicado:", r0["radicado"])
print("URL doc:", url[:110], "...\n")

resp = requests.get(url, headers=HEADERS, timeout=60, allow_redirects=True)
print("STATUS:", resp.status_code)
print("Content-Type:", resp.headers.get("Content-Type"))
print("Content-Length:", resp.headers.get("Content-Length"), "| bytes reales:", len(resp.content))
print("URL final:", resp.url[:110])
ct = resp.headers.get("Content-Type", "")
if "html" in ct:
    with open("doc_sample.html", "w", encoding="utf-8") as f:
        f.write(resp.text)
    print(">> guardado doc_sample.html")
    low = resp.text.lower()
    for k in ["iframe", ".pdf", "embed", "tokendocumento", "src="]:
        print(f"   contiene '{k}':", k in low)
elif "pdf" in ct:
    with open("doc_sample.pdf", "wb") as f:
        f.write(resp.content)
    print(">> guardado doc_sample.pdf (es PDF directo!)")
else:
    print(">> otro tipo:", ct)
    print(resp.text[:300])
