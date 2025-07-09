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
    command: ["/busybox/cat"]   # keeps the container alive for Jenkins to exec into it
    tty: true
"""
    }
  }

  environment {
    // Registry service inside the cluster (port 5000 on the Cluster-IP service)
    IMAGE_DEST = "registry-docker-registry.registry.svc.cluster.local:5000/sgu:test"
    // short Git SHA (first 7 chars) provided by Jenkins variable GIT_COMMIT
    GIT_SHA = "${env.GIT_COMMIT.take(7)}"
  }

  stages {
    stage('Build & Push with Kaniko') {
      steps {
        container(name: 'kaniko', shell: '/busybox/sh') {
          sh """
            /kaniko/executor \
              --context=\$(pwd) \
              --dockerfile=Dockerfile \
              --destination=\$IMAGE_BASE:\$GIT_SHA \
              --destination=\$IMAGE_BASE:latest \\
              --insecure \
              --skip-tls-verify
          """
        }
      }
    }
  }
}
