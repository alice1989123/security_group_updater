pipeline {
  agent {
    kubernetes {
      defaultContainer 'kaniko'
      yaml """ (same YAML block) """
    }
  }

  environment {
    // short Git SHA (first 7 chars) provided by Jenkins variable GIT_COMMIT
    GIT_SHA = "${env.GIT_COMMIT.take(7)}"
    // registry URL for all immutable images
    IMAGE_BASE = "registry-docker-registry.registry.svc.cluster.local:5000/sgu"
  }

  stages {
    stage('Build & push') {
      steps {
        container(name: 'kaniko', shell: '/busybox/sh') {
          sh """
            /kaniko/executor \
              --context=\$(pwd) \
              --dockerfile=Dockerfile \
              --destination=\$IMAGE_BASE:\$GIT_SHA \
              --destination=\$IMAGE_BASE:latest \\
              --insecure --skip-tls-verify
          """
        }
      }
    }
  }

  post {
    success {
      echo "Pushed \$IMAGE_BASE:\$GIT_SHA and :latest"
    }
  }
}
