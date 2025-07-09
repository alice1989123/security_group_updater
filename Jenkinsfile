podTemplate(yaml: """
apiVersion: v1
kind: Pod
metadata:
  name: kaniko
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    args:
      - "--help"   # valid dummy arg, doesn't crash
    volumeMounts:
      - name: kaniko-secret
        mountPath: /kaniko/.docker/
  restartPolicy: Never
  volumes:
    - name: kaniko-secret
      secret:
        secretName: kaniko-docker-config
""") {
  node(POD_LABEL) {
    stage('Build') {
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
