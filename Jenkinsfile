gcr.io/kaniko-project/executor:debug         # “latest” debug
gcr.io/kaniko-project/executor:v1.24.0-debug # version-pinned debug (recommended)
``` :contentReference[oaicite:0]{index=0}

That debug image contains:

* **/busybox/sh** and **/busybox/cat**  
* a minimal `PATH` (so you often need `shell: '/busybox/sh'` or `PATH+EXTRA=/busybox`)

---

## Updated declarative pipeline (uses the current debug tag)

```groovy
pipeline {
  agent {
    kubernetes {
      defaultContainer 'kaniko'
      yaml """
apiVersion: v1
kind: Pod
metadata:
  name: kaniko
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:v1.24.0-debug   # ← debug tag with BusyBox
    imagePullPolicy: IfNotPresent
    command: [/busybox/cat]                               # keep the pod alive
    tty: true
    volumeMounts:
      - name: docker-cfg
        mountPath: /kaniko/.docker
  volumes:
  - name: docker-cfg
    projected:
      sources:
      - secret:
          name: docker-credentials
          items:
          - key: .dockerconfigjson
            path: config.json
"""
    }
  }

  environment {
    IMAGE_DEST = "registry.local:31504/security_group_updater:prod"
  }

  stages {
    stage('Build with Kaniko') {
      steps {
        checkout scm
        container(name: 'kaniko', shell: '/busybox/sh') {
          withEnv(['PATH+EXTRA=/busybox']) {
            sh '''
              /kaniko/executor \
                --context `pwd` \
                --dockerfile Dockerfile \
                --destination $IMAGE_DEST \
                --insecure --skip-tls-verify
            '''
          }
        }
      }
    }
  }
}
