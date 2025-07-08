podTemplate(yaml: """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
      - cat            # keeps the container running
    tty: true          # <-- required when command is cat
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
