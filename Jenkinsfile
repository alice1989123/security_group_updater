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
      command:
        - /kaniko/executor
      args:
        - --context=git://github.com/alice1989123/security_group_updater.git
        - --dockerfile=Dockerfile
        - --destination=registry-docker-registry.registry.svc.cluster.local:5000/security_group_updater:prod_v2
        - --insecure
        - --skip-tls-verify
      volumeMounts:
        - name: kaniko-secret
          mountPath: /kaniko/.docker
    - name: kubectl
      image: bitnami/kubectl:latest
      command:
        - cat
      tty: true
  volumes:
    - name: kaniko-secret
      emptyDir: {}
"""
        }
    }
    stages {
        
        stage('Build with Kaniko') {
          steps {
              container('kaniko') {
                  sh '''
                  /kaniko/executor \
                    --context=https://github.com/alice1989123/security_group_updater.git \
                    --dockerfile=Dockerfile \
                    --destination=registry.local:31504/security_group_updater:prod \
                    --insecure \
                    --skip-tls-verify
                  '''
              }
          }
      }

 
    }
}
