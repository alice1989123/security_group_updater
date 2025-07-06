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
        - cat
      tty: true
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
                    sh '''
                    /kaniko/executor \
                      --context=${WORKSPACE} \
                      --dockerfile=Dockerfile \
                      --destination=registry-docker-registry.registry.svc.cluster.local:5000/security_group_updater:prod \
                      --insecure \
                      --skip-tls-verify
                    '''
                }
            }
        }
    }
}
