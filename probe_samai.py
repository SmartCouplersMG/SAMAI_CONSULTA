"""Sondeo real de SAMAI: ejecuta una busqueda rapida y captura la estructura
de resultados para mapear la extraccion. No es el scraper final, es reconocimiento.
"""
from playwright.sync_api import sync_playwright

URL = ("https://samai.consejodeestado.gov.co/"
       "TitulacionRelatoria/BuscadorProvidenciasTituladas.aspx")
TERMINO = "contrato estatal"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent=(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"))
    page.set_default_timeout(45000)

    def settle(msg):
        try:
            page.wait_for_load_state("networkidle", timeout=45000)
        except Exception as e:
            print(f"   (timeout networkidle en {msg})", e)
        page.wait_for_timeout(2500)

    print(">> Cargando pagina...")
    page.goto(URL, wait_until="networkidle")
    print("   Titulo:", page.title())

    # PASO 1: seleccionar Corporacion = Consejo de Estado
    print(">> Seleccionando Corporacion: Consejo de Estado")
    page.click("#MainContent_CorporacionesTitulanDataList_CorporacionButton_0")
    settle("seleccion corporacion")

    # PASO 2: busqueda rapida
    print(">> Escribiendo termino:", TERMINO)
    page.fill("#BusquedaRapidaTextBox", f'"{TERMINO}"')
    page.evaluate("__doPostBack('ctl00$MainContent$BusquedaRapidaLinkButton','')")
    settle("agregar termino")

    # PASO 3: ejecutar y ver resultados
    print(">> Ejecutando busqueda (Ver resultados)...")
    page.evaluate("__doPostBack('ctl00$MainContent$BuscarProvidenciasLinkButton','')")
    settle("ver resultados")
    page.wait_for_timeout(3000)

    # Guardar evidencia
    html = page.content()
    with open("samai_resultados.html", "w", encoding="utf-8") as f:
        f.write(html)
    page.screenshot(path="samai_resultados.png", full_page=True)
    print(">> Guardados: samai_resultados.html / .png  (len=%d)" % len(html))

    # Heuristica: buscar enlaces a providencias / PDFs
    enlaces = page.eval_on_selector_all(
        "a",
        """els => els.map(a => ({texto: (a.innerText||'').trim().slice(0,80),
                                  href: a.getAttribute('href')||''}))
              .filter(x => x.href && (x.href.toLowerCase().includes('.pdf')
                       || x.href.toLowerCase().includes('providencia')
                       || x.href.toLowerCase().includes('documento')
                       || x.href.toLowerCase().includes('verprov')))""")
    print(">> Enlaces candidatos (PDF/providencia):", len(enlaces))
    for e in enlaces[:15]:
        print("   -", e["texto"], "=>", e["href"][:90])

    browser.close()
print(">> FIN sondeo")
