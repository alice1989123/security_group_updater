pipeline {
  agent {
    kubernetes {
      defaultContainer 'kaniko'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:v1.24.0-debug
    command: ["/busybox/cat"]
    tty: true
"""
    }
  }

  stages {
    stage('Build') {
      steps {
        container(name: 'kaniko', shell: '/busybox/sh') {
          sh '''
            /kaniko/executor \
              --context=`pwd` \
              --dockerfile=Dockerfile \
              --destination=registry.local:31504/sgu:test \
              --insecure \
              --skip-tls-verify
          '''
        }
      }
    }
  }
}
