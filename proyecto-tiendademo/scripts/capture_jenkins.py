"""Capture the local Jenkins UI for the documented build."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(root / ".cache/ms-playwright"))
folders = list((root / "evidencias/jenkins").glob("build-*"))
folder = max(folders, key=lambda path: int(path.name.split("-")[1]))
summary = json.loads((folder / "resumen.json").read_text())
with sync_playwright() as manager:
    browser = manager.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.goto("http://127.0.0.1:8081/login")
    page.locator('input[name="j_username"]').fill("admin")
    page.locator('input[name="j_password"]').fill((root / ".jenkins-local/admin-password").read_text().strip())
    page.locator('button[type="submit"], input[type="submit"]').first.click()
    page.wait_for_load_state("networkidle")
    for name, url in [
        ("01-trabajo.png", "http://127.0.0.1:8081/job/TiendaDemo-Pruebas/"),
        ("02-build.png", summary["url"]),
        ("03-consola.png", summary["url"] + "console"),
        ("04-artefactos.png", summary["url"] + "artifact/"),
    ]:
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page.screenshot(path=str(folder / name), full_page=True)
    browser.close()
print(f"Capturas guardadas en {folder}")
