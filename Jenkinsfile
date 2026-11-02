
pipeline {
    agent any

    parameters {
        booleanParam(
            name: 'PRUEBAS_FUNCIONALES',
            defaultValue: false,
            description: 'Ejecutar Selenium y Playwright'
        )

        booleanParam(
            name: 'PRUEBAS_K6',
            defaultValue: false,
            description: 'Ejecutar las pruebas largas de rendimiento y estres'
        )
    }

    environment {
        PATH = "/Applications/Docker.app/Contents/Resources/bin:/usr/local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:${env.PATH}"

        TIENDA_URL = "http://127.0.0.1:8082/tienda_demo.html"
        AULA_NOVA_URL = "http://127.0.0.1:3003"

        DOCKER_BUILDKIT = "1"
    }

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 120, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Descargar proyecto GitHub') {
            steps {
                checkout scm
            }
        }

        stage('Preparar directorios') {
            steps {
                sh '''
                    set -eu

                    mkdir -p proyecto-tiendademo/reports/jenkins
                    mkdir -p aula-nova-semana9/reports/servidor
                    mkdir -p aula-nova-semana9/reports/seguridad
                    mkdir -p aula-nova-semana9/reports/pytest
                    mkdir -p aula-nova-semana9/reports/performance
                    mkdir -p aula-nova-semana9/reports/stress

                    echo "Directorios preparados."
                '''
            }
        }

        stage('Verificar herramientas') {
            steps {
                sh '''
                    set -eu

                    echo "=== DOCKER ==="
                    docker --version
                    docker compose version
                    docker info > /dev/null

                    echo "=== NODE ==="
                    node --version
                    npm --version

                    echo "=== PYTHON ==="
                    python3 --version

                    echo "Herramientas verificadas."
                '''
            }
        }

        stage('Preparar Compose aislado') {
            steps {
                sh '''
                    set -eu

                    python3 - <<'PY'
from pathlib import Path

p8 = Path("docker-compose.semana8.yml")
p9 = Path("docker-compose.semana9.yml")

a = p8.read_text()
b = p9.read_text()

assert "8081:80" in a
assert "3001:3000" in b

a = a.replace(
    "8081:80",
    "127.0.0.1:8082:80"
)

b = b.replace(
    "3001:3000",
    "127.0.0.1:3003:3000"
)

b = b.replace(
    "container_name: aula-nova-semana09",
    ""
)

Path("ci-semana8.yml").write_text(a)
Path("ci-semana9.yml").write_text(b)

print("Compose CI preparado.")
PY
                '''
            }
        }

        stage('Construir Docker Semana 8') {
            steps {
                sh '''
                    set -eu

                    docker compose -p semana11ci8 \
                      -f ci-semana8.yml build
                '''
            }
        }

        stage('Iniciar TiendaDemo') {
            steps {
                sh '''
                    set -eu

                    docker compose -p semana11ci8 \
                      -f ci-semana8.yml up -d

                    python3 scripts/wait_http.py \
                      "$TIENDA_URL"

                    echo "TiendaDemo disponible."
                '''
            }
        }

        stage('Construir Docker Semana 9') {
            steps {
                sh '''
                    set -eu

                    docker compose -p semana11ci9 \
                      -f ci-semana9.yml build
                '''
            }
        }

        stage('Iniciar Aula Nova') {
            steps {
                sh '''
                    set -eu

                    docker compose -p semana11ci9 \
                      -f ci-semana9.yml up -d

                    python3 scripts/wait_http.py \
                      "$AULA_NOVA_URL/api/courses"

                    echo "Aula Nova disponible."
                '''
            }
        }

        stage('Pruebas API Semana 9') {
            steps {
                catchError(
                    buildResult: 'FAILURE',
                    stageResult: 'FAILURE'
                ) {
                    dir('aula-nova-semana9') {
                        sh '''
                            set -eu

                            node --test \
                              --test-reporter=junit \
                              --test-reporter-destination=reports/servidor/TESTS-servidor.xml \
                              backend/server.test.js

                            echo "Reporte del servidor generado."
                        '''
                    }
                }
            }
        }

        stage('Pruebas seguridad Semana 9') {
            steps {
                catchError(
                    buildResult: 'FAILURE',
                    stageResult: 'FAILURE'
                ) {
                    dir('aula-nova-semana9') {
                        sh '''
                            set -eu

                            node --test \
                              --test-reporter=junit \
                              --test-reporter-destination=reports/seguridad/TESTS-seguridad.xml \
                              backend/security.test.js

                            echo "Reporte de seguridad generado."
                        '''
                    }
                }
            }
        }

        stage('Pruebas funcionales Semana 8') {
            when {
                expression {
                    return params.PRUEBAS_FUNCIONALES
                }
            }

            steps {
                catchError(
                    buildResult: 'FAILURE',
                    stageResult: 'FAILURE'
                ) {
                    dir('proyecto-tiendademo') {
                        sh '''
                            set -eu

                            python3 -m venv .venv

                            .venv/bin/python -m pip install \
                              -r requirements.txt

                            .venv/bin/python -m playwright \
                              install chromium

                            export BASE_URL="$TIENDA_URL"

                            .venv/bin/python -m pytest \
                              selenium/tests \
                              -v \
                              --junitxml=reports/jenkins/selenium.xml

                            .venv/bin/python -m pytest \
                              playwright/tests \
                              -v \
                              --junitxml=reports/jenkins/playwright.xml
                        '''
                    }
                }
            }
        }

        stage('Pruebas funcionales Semana 9') {
            when {
                expression {
                    return params.PRUEBAS_FUNCIONALES
                }
            }

            steps {
                catchError(
                    buildResult: 'FAILURE',
                    stageResult: 'FAILURE'
                ) {
                    dir('aula-nova-semana9') {
                        sh '''
                            set -eu

                            python3 -m venv .venv

                            .venv/bin/python -m pip install \
                              pytest playwright

                            .venv/bin/python -m playwright \
                              install chromium

                            export BASE_URL="$AULA_NOVA_URL"

                            .venv/bin/python -m pytest \
                              tests \
                              -v \
                              --junitxml=reports/pytest/TESTS-playwright.xml
                        '''
                    }
                }
            }
        }

        stage('Rendimiento k6 Semana 9') {
            when {
                expression {
                    return params.PRUEBAS_K6
                }
            }

            steps {
                catchError(
                    buildResult: 'FAILURE',
                    stageResult: 'FAILURE'
                ) {
                    dir('aula-nova-semana9') {
                        sh '''
                            set -eu

                            k6 version

                            for i in $(seq -w 1 10); do
                                echo "Ejecutando CR-$i"

                                k6 run \
                                  --env BASE_URL="$AULA_NOVA_URL" \
                                  --summary-export="reports/performance/CR-$i.json" \
                                  "prueba-rendimiento/CR-$i.js"
                            done
                        '''
                    }
                }
            }
        }

        stage('Estres k6 Semana 9') {
            when {
                expression {
                    return params.PRUEBAS_K6
                }
            }

            steps {
                catchError(
                    buildResult: 'FAILURE',
                    stageResult: 'FAILURE'
                ) {
                    dir('aula-nova-semana9') {
                        sh '''
                            set -eu

                            for i in $(seq -w 1 10); do
                                echo "Ejecutando CE-$i"

                                k6 run \
                                  --env BASE_URL="$AULA_NOVA_URL" \
                                  --summary-export="reports/stress/CE-$i.json" \
                                  "pruebas-estres/CE-$i.js"
                            done
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            sh '''
                mkdir -p proyecto-tiendademo/reports/jenkins
                mkdir -p aula-nova-semana9/reports

                if [ -f ci-semana8.yml ]; then
                    docker compose -p semana11ci8 \
                      -f ci-semana8.yml logs --no-color \
                      > proyecto-tiendademo/reports/jenkins/docker-compose.log 2>&1 || true

                    docker compose -p semana11ci8 \
                      -f ci-semana8.yml down --remove-orphans || true
                fi

                if [ -f ci-semana9.yml ]; then
                    docker compose -p semana11ci9 \
                      -f ci-semana9.yml logs --no-color \
                      > aula-nova-semana9/reports/docker-compose.log 2>&1 || true

                    docker compose -p semana11ci9 \
                      -f ci-semana9.yml down --remove-orphans || true
                fi
            '''

            junit(
                testResults: 'proyecto-tiendademo/reports/jenkins/*.xml,aula-nova-semana9/reports/**/*.xml',
                allowEmptyResults: true
            )

            archiveArtifacts(
                artifacts: 'proyecto-tiendademo/reports/jenkins/**/*,aula-nova-semana9/reports/**/*',
                allowEmptyArchive: true
            )
        }

        success {
            echo 'SEMANA 11: PIPELINE FINALIZADO CORRECTAMENTE'
        }

        failure {
            echo 'SEMANA 11: SE DETECTARON ERRORES'
        }
    }
}
