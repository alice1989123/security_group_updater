pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: kaniko
      image: gcr.io/kaniko-project/executor:latest
      # ENTRYPOINT = /kaniko/executor
      args:
        - --context=https://github.com/alice1989123/security_group_updater.git
        - --dockerfile=Dockerfile
        - --destination=registry.local:31504/security_group_updater:prod
        - --insecure
        - --skip-tls-verify
      tty: true
"""
    }
  }

  stages {
    stage('Build & Push') {
      steps {
        container('kaniko') {
          echo 'Kaniko está construyendo la imagen…'
          /* No hay que ejecutar nada: el contenedor ya lo hace en su arranque. */
        }
      }
    }
  }
}