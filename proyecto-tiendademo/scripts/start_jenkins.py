"""Start the project-local Jenkins controller with a private admin account."""
import os
from pathlib import Path
import secrets
import socket
import subprocess

root = Path(__file__).resolve().parents[1]
with socket.socket() as probe:
    if probe.connect_ex(("127.0.0.1", 8081)) == 0:
        raise SystemExit("El puerto 8081 ya esta ocupado. No se inicia una segunda instancia.")
local = root / ".jenkins-local"
home = local / "home"
home.mkdir(parents=True, exist_ok=True)
credential = local / "admin-password"
if not credential.exists():
    fd = os.open(credential, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as stream:
        stream.write(secrets.token_urlsafe(24))
init = home / "init.groovy.d"
init.mkdir(exist_ok=True)
(init / "tiendademo.groovy").write_text((root / "scripts/jenkins-init.groovy").read_text())
java = next((local / "runtime").glob("*/Contents/Home/bin/java"))
env = dict(os.environ, JENKINS_HOME=str(home), TIENDADEMO_ROOT=str(root))
command = [str(java), "-Djenkins.install.runSetupWizard=false", "-jar",
           str(local / "runtime/jenkins.war"), "--httpListenAddress=127.0.0.1", "--httpPort=8081"]
log = open(local / "jenkins.log", "ab")
process = subprocess.Popen(command, env=env, stdout=log, stderr=log, start_new_session=True)
(local / "jenkins.pid").write_text(str(process.pid))
print(f"Jenkins PID: {process.pid}; URL: http://127.0.0.1:8081")
print(f"Usuario: admin; clave privada: {credential}")
