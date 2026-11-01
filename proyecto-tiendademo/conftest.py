# Cargar las bibliotecas antes de que Pytest use los nombres de las carpetas.
import selenium
import playwright
import importlib.util
import os
from pathlib import Path
from datetime import datetime
import pytest

ROOT = Path(__file__).parent
os.environ.setdefault("SE_CACHE_PATH", str(ROOT / ".cache/selenium"))
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(ROOT / ".cache/ms-playwright"))

def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="Mostrar el navegador")

@pytest.fixture(scope="session")
def evidence_run():
    return datetime.now().strftime("%Y%m%d-%H%M%S-%f")

@pytest.fixture
def tienda(request, evidence_run):
    framework = "selenium" if "selenium" in str(request.node.path) else "playwright"
    from utils.ui_adapters import SeleniumUI, PlaywrightUI
    url = os.getenv("BASE_URL", (ROOT / "app/tienda_demo.html").as_uri())
    headed = request.config.getoption("--headed")
    if framework == "selenium":
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        if not headed:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1100")
        driver = webdriver.Chrome(options=options)
        ui = SeleniumUI(driver)
        close = driver.quit
        driver.get(url)
    else:
        from playwright.sync_api import sync_playwright
        manager = sync_playwright().start()
        try:
            browser = manager.chromium.launch(headless=not headed)
            page = browser.new_page(viewport={"width":1440, "height":1100})
            ui = PlaywrightUI(page)
            page.goto(url)
        except Exception:
            manager.stop()
            raise
        def close():
            browser.close()
            manager.stop()
    objects = []
    try:
        for module, cls in [("catalogo_page", "CatalogoPage"), ("cart_page", "CartPage"), ("checkout_page", "CheckoutPage")]:
            spec = importlib.util.spec_from_file_location(f"{framework}_{module}", ROOT / framework / "pages" / f"{module}.py")
            loaded = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(loaded)
            objects.append(getattr(loaded, cls)(ui))
        yield tuple(objects)
    finally:
        folder = Path(os.getenv("EVIDENCE_DIR", str(ROOT / "evidencias"))) / framework / evidence_run
        folder.mkdir(parents=True, exist_ok=True)
        try:
            ui.screenshot(folder / f"{request.node.name}.png")
        finally:
            close()
