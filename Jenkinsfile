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
      # ⇢ ENTRYPOINT del image = /kaniko/executor
      #    Le pasamos los flags en 'args', por lo que al arrancar
      #    el contenedor ya hace el build & push y luego sale.
      args:
        - --context=https://github.com/alice1989123/security_group_updater.git
        - --dockerfile=Dockerfile
        - --destination=registry.local:31504/security_group_updater:prod    # o svc.cluster.local:5000
        - --insecure
        - --skip-tls-verify
      volumeMounts:                     # opcional si usas cred-helpers
        - name: kaniko-secret
          mountPath: /kaniko/.docker
      tty: true                         # <- mantiene STDIN abierto para logs
    - name: kubectl                     # por si luego lo necesitas
      image: bitnami/kubectl:latest
      command: [ "cat" ]
      tty: true
  volumes:
    - name: kaniko-secret
      emptyDir: {}
"""
    }
  }

  stages {
    stage('Build & Push') {
      steps {
        /*  No hace falta llamar a /kaniko/executor aquí:
            el contenedor ya lo está ejecutando al arrancar.
            Sólo esperamos a que termine y vemos los logs. */
        container('kaniko') {
          echo 'Kaniko está construyendo y empujando la imagen…'
        }
      }
    }
  }
}