"""Run the local Jenkins job and export genuine build evidence."""
import base64
from http.cookiejar import CookieJar
import json
from pathlib import Path
import time
from urllib.request import build_opener, HTTPCookieProcessor, Request
import xml.etree.ElementTree as ET
import zipfile

root = Path(__file__).resolve().parents[1]
target = root / "evidencias/jenkins"
target.mkdir(parents=True, exist_ok=True)
password = (root / ".jenkins-local/admin-password").read_text().strip()
auth = base64.b64encode(f"admin:{password}".encode()).decode()
opener = build_opener(HTTPCookieProcessor(CookieJar()))
base = "http://127.0.0.1:8081"


def fetch(path, data=None, extra=None):
    headers = {"Authorization": f"Basic {auth}", **(extra or {})}
    return opener.open(Request(base + path, data=data, headers=headers), timeout=30)


crumb = json.load(fetch("/crumbIssuer/api/json"))
response = fetch("/job/TiendaDemo-Pruebas/build", b"", {crumb["crumbRequestField"]: crumb["crumb"]})
queue_path = response.headers["Location"].removeprefix(base).rstrip("/")
deadline = time.monotonic() + 1800
build = None
while time.monotonic() < deadline:
    queued = json.load(fetch(queue_path + "/api/json"))
    if queued.get("cancelled"):
        raise RuntimeError("Jenkins cancelled the build")
    if "executable" in queued:
        build = queued["executable"]["number"]
        break
    time.sleep(2)
if build is None:
    raise TimeoutError("Build did not start")
print(f"Build #{build} iniciado", flush=True)
build_path = f"/job/TiendaDemo-Pruebas/{build}"
while time.monotonic() < deadline:
    result = json.load(fetch(build_path + "/api/json"))
    if not result["building"]:
        break
    time.sleep(5)
else:
    raise TimeoutError("Build did not finish")
folder = target / f"build-{build}"
folder.mkdir(exist_ok=True)
(folder / "build.json").write_text(json.dumps(result, indent=2))
(folder / "consola.log").write_bytes(fetch(build_path + "/consoleText").read())
counts = {}
for framework in ("selenium", "playwright"):
    data = fetch(build_path + f"/artifact/evidencias/{build}/{framework}/resultados.xml").read()
    (folder / f"{framework}-resultados.xml").write_bytes(data)
    suites = ET.fromstring(data).iter("testsuite")
    counts[framework] = {key: 0 for key in ("tests", "failures", "errors", "skipped")}
    for suite in suites:
        for key in counts[framework]:
            counts[framework][key] += int(suite.get(key, 0))
summary = {"build": build, "result": result["result"], "url": base + build_path + "/", "suites": counts}
(folder / "resumen.json").write_text(json.dumps(summary, indent=2))
archive = fetch(build_path + "/artifact/*zip*/archive.zip").read()
(folder / "artefactos.zip").write_bytes(archive)
with zipfile.ZipFile(folder / "artefactos.zip") as zipped:
    print(f"Artefactos: {len(zipped.namelist())} entradas", flush=True)
print(json.dumps(summary, indent=2), flush=True)
if result["result"] != "SUCCESS":
    raise SystemExit(1)
