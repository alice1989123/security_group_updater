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
    command: ["/busybox/cat"]      # keep the container alive for Jenkins exec
    tty: true
"""
    }
  }

  /* Base repository URL in your registry */
  environment {
    IMAGE_BASE = 'registry-docker-registry.registry.svc.cluster.local:5000/security_group_updater'
  }

  stages {

    stage('Build & push') {
      steps {
        /* 1️⃣  determine the short commit SHA **after** checkout */
        script {
          env.GIT_SHA = sh(
            script: 'git rev-parse --short=7 HEAD',
            returnStdout: true
          ).trim()
          echo "Building tag: ${env.GIT_SHA}"
        }

        /* 2️⃣  run Kaniko */
        container(name: 'kaniko', shell: '/busybox/sh') {
          sh '''
            /kaniko/executor \
              --context=$(pwd) \
              --dockerfile=Dockerfile \
              --destination=$IMAGE_BASE:$GIT_SHA \
              --destination=$IMAGE_BASE:latest \
              --label org.opencontainers.image.revision=$GIT_SHA \
              --insecure \
              --skip-tls-verify
          '''
        }
      }
    }
  }

  post {
    success {
      echo "✅ Pushed $IMAGE_BASE:$GIT_SHA and $IMAGE_BASE:latest"
    }
  }
}
