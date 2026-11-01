import jenkins.model.Jenkins
import hudson.model.FreeStyleProject
import hudson.tasks.Shell
import hudson.tasks.ArtifactArchiver
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import jenkins.install.InstallState

def instance = Jenkins.get()
def root = System.getenv('TIENDADEMO_ROOT')
def realm = new HudsonPrivateSecurityRealm(false)
if (instance.getSecurityRealm() instanceof HudsonPrivateSecurityRealm) {
    realm = instance.getSecurityRealm()
}
if (hudson.model.User.getById('admin', false) == null) {
    realm.createAccount('admin', new File(root, '.jenkins-local/admin-password').text.trim())
}
instance.setSecurityRealm(realm)
def authorization = new FullControlOnceLoggedInAuthorizationStrategy()
authorization.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(authorization)
instance.setNumExecutors(1)
instance.setInstallState(InstallState.INITIAL_SETUP_COMPLETED)
def name = 'TiendaDemo-Pruebas'
if (instance.getItem(name) == null) {
    def job = instance.createProject(FreeStyleProject, name)
    job.setDescription('Pruebas locales de TiendaDemo: Selenium y Playwright. XML, logs y capturas en los artefactos de cada build.')
    def quotedRoot = "'" + root.replace("'", "'\\''") + "'"
    job.getBuildersList().add(new Shell('''#!/bin/bash
set -eu
export EVIDENCE_DIR="$WORKSPACE/evidencias/$BUILD_NUMBER"
export CI_SKIP_INSTALL=1
''' + 'export CI_PYTHON=' + quotedRoot + '/.venv/bin/python\n' + 'bash ' + quotedRoot + '/scripts/ci.sh\n'))
    def archiver = new ArtifactArchiver('evidencias/**/*')
    archiver.setAllowEmptyArchive(false)
    job.getPublishersList().add(archiver)
    job.save()
}
instance.save()
