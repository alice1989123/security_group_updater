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
        - --destination=registry-docker-registry.registry.svc.cluster.local:5000/security_group_updater:prod
        - --insecure
        - --skip-tls-verify
      volumeMounts:
        - name: kaniko-secret
          mountPath: /kaniko/.docker
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
                    echo 'Build finished.'
                }
            }
        }
    }
}
