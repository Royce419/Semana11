def runCommand(String unixCommand, String windowsCommand) {
    if (isUnix()) {
        sh(script: unixCommand)
    } else {
        bat(script: windowsCommand)
    }
}

pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 120, unit: 'MINUTES')
    }

    environment {
        TIENDA_URL = 'http://127.0.0.1:8081/tienda_demo.html'
        AULA_NOVA_URL = 'http://127.0.0.1:3001'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verificar herramientas') {
            steps {
                script {
                    runCommand(
                        'docker compose version && node --version && python3 --version && k6 version',
                        'docker compose version && node --version && py --version && k6 version'
                    )
                }
            }
        }

        stage('Preparar Semana 8') {
            steps {
                dir('proyecto-tiendademo') {
                    script {
                        runCommand(
                            'python3 -m pip install -r requirements.txt && python3 -m playwright install chromium',
                            'py -m pip install -r requirements.txt && py -m playwright install chromium'
                        )
                    }
                }
            }
        }

        stage('Build y entorno Docker Semana 8') {
            steps {
                script {
                    runCommand(
                        'docker compose -f docker-compose.semana8.yml up -d --build',
                        'docker compose -f docker-compose.semana8.yml up -d --build'
                    )
                }
            }
        }

        stage('Esperar TiendaDemo') {
            steps {
                script {
                    runCommand(
                        'python3 scripts/wait_http.py http://127.0.0.1:8081/tienda_demo.html',
                        'py scripts/wait_http.py http://127.0.0.1:8081/tienda_demo.html'
                    )
                }
            }
        }

        stage('Selenium Semana 8') {
            steps {
                dir('proyecto-tiendademo') {
                    script {
                        withEnv(["BASE_URL=${env.TIENDA_URL}", "EVIDENCE_DIR=${env.WORKSPACE}/proyecto-tiendademo/evidencias/jenkins-${env.BUILD_NUMBER}"]) {
                            runCommand(
                                'mkdir -p reports/jenkins && python3 -m pytest selenium/tests -v --junitxml=reports/jenkins/selenium.xml',
                                'if not exist reports\\jenkins mkdir reports\\jenkins\r\npy -m pytest selenium/tests -v --junitxml=reports/jenkins/selenium.xml'
                            )
                        }
                    }
                }
            }
        }

        stage('Playwright Semana 8') {
            steps {
                dir('proyecto-tiendademo') {
                    script {
                        withEnv(["BASE_URL=${env.TIENDA_URL}", "EVIDENCE_DIR=${env.WORKSPACE}/proyecto-tiendademo/evidencias/jenkins-${env.BUILD_NUMBER}"]) {
                            runCommand(
                                'mkdir -p reports/jenkins && python3 -m pytest playwright/tests -v --junitxml=reports/jenkins/playwright.xml',
                                'if not exist reports\\jenkins mkdir reports\\jenkins\r\npy -m pytest playwright/tests -v --junitxml=reports/jenkins/playwright.xml'
                            )
                        }
                    }
                }
            }
        }

        stage('Preparar Semana 9') {
            steps {
                dir('aula-nova-semana9') {
                    script {
                        runCommand(
                            'npm ci && python3 -m pip install pytest playwright && python3 -m playwright install chromium && mkdir -p reports/servidor reports/pytest reports/seguridad reports/performance reports/stress',
                            'npm ci && py -m pip install pytest playwright && py -m playwright install chromium && if not exist reports\\servidor mkdir reports\\servidor && if not exist reports\\pytest mkdir reports\\pytest && if not exist reports\\seguridad mkdir reports\\seguridad && if not exist reports\\performance mkdir reports\\performance && if not exist reports\\stress mkdir reports\\stress'
                        )
                    }
                }
            }
        }

        stage('Build y entorno Docker Semana 9') {
            steps {
                script {
                    runCommand(
                        'docker compose -f docker-compose.semana9.yml up -d --build',
                        'docker compose -f docker-compose.semana9.yml up -d --build'
                    )
                }
            }
        }

        stage('Esperar Aula Nova') {
            steps {
                script {
                    runCommand(
                        'python3 scripts/wait_http.py http://127.0.0.1:3001/api/courses',
                        'py scripts/wait_http.py http://127.0.0.1:3001/api/courses'
                    )
                }
            }
        }

        stage('Pruebas servidor y seguridad Semana 9') {
            steps {
                dir('aula-nova-semana9') {
                    script {
                        runCommand(
                            'node --test --test-reporter=junit --test-reporter-destination=reports/servidor/TESTS-servidor.xml backend/server.test.js && node --test --test-reporter=junit --test-reporter-destination=reports/seguridad/TESTS-seguridad.xml backend/security.test.js',
                            'node --test --test-reporter=junit --test-reporter-destination=reports/servidor/TESTS-servidor.xml backend/server.test.js && node --test --test-reporter=junit --test-reporter-destination=reports/seguridad/TESTS-seguridad.xml backend/security.test.js'
                        )
                    }
                }
            }
        }

        stage('Pruebas funcionales Semana 9') {
            steps {
                dir('aula-nova-semana9') {
                    script {
                        withEnv(["BASE_URL=${env.AULA_NOVA_URL}"]) {
                            runCommand(
                                'python3 -m pytest tests -v --junitxml=reports/pytest/TESTS-playwright.xml',
                                'py -m pytest tests -v --junitxml=reports/pytest/TESTS-playwright.xml'
                            )
                        }
                    }
                }
            }
        }

        stage('Pruebas de rendimiento k6') {
            steps {
                dir('aula-nova-semana9') {
                    script {
                        for (int i = 1; i <= 10; i++) {
                            String id = String.format('%02d', i)
                            runCommand(
                                "k6 run --env BASE_URL=${env.AULA_NOVA_URL} --summary-export=reports/performance/CR-${id}.json prueba-rendimiento/CR-${id}.js",
                                "k6 run --env BASE_URL=${env.AULA_NOVA_URL} --summary-export=reports\\performance\\CR-${id}.json prueba-rendimiento\\CR-${id}.js"
                            )
                        }
                    }
                }
            }
        }

        stage('Pruebas de estrés k6') {
            steps {
                dir('aula-nova-semana9') {
                    script {
                        for (int i = 1; i <= 10; i++) {
                            String id = String.format('%02d', i)
                            runCommand(
                                "k6 run --env BASE_URL=${env.AULA_NOVA_URL} --summary-export=reports/stress/CE-${id}.json pruebas-estres/CE-${id}.js",
                                "k6 run --env BASE_URL=${env.AULA_NOVA_URL} --summary-export=reports\\stress\\CE-${id}.json pruebas-estres\\CE-${id}.js"
                            )
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                runCommand(
                    'docker compose -f docker-compose.semana9.yml logs --no-color > aula-nova-semana9/reports/docker-compose.log 2>&1 || true; docker compose -f docker-compose.semana9.yml down --remove-orphans || true; docker compose -f docker-compose.semana8.yml logs --no-color > proyecto-tiendademo/reports/jenkins/docker-compose.log 2>&1 || true; docker compose -f docker-compose.semana8.yml down --remove-orphans || true',
                    'docker compose -f docker-compose.semana9.yml logs --no-color > aula-nova-semana9\\reports\\docker-compose.log 2>&1 & docker compose -f docker-compose.semana9.yml down --remove-orphans & docker compose -f docker-compose.semana8.yml logs --no-color > proyecto-tiendademo\\reports\\jenkins\\docker-compose.log 2>&1 & docker compose -f docker-compose.semana8.yml down --remove-orphans'
                )
            }
            junit testResults: 'proyecto-tiendademo/reports/jenkins/*.xml', allowEmptyResults: true
            junit testResults: 'aula-nova-semana9/reports/**/*.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'proyecto-tiendademo/reports/jenkins/**/*,proyecto-tiendademo/evidencias/jenkins-*/**,aula-nova-semana9/reports/**/*,aula-nova-semana9/evidencias/**/*', allowEmptyArchive: true
        }
    }
}
