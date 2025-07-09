podTemplate(yaml: """\
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command: ["/kaniko/executor"]
    args:
      - "--context=git://github.com/alice1989123/security_group_updater.git"
      - "--dockerfile=Dockerfile"
      - "--destination=registry.local:31504/security_group_updater:prod"
      - "--insecure"
      - "--skip-tls-verify"
  restartPolicy: Never
""") {
  node(POD_LABEL) {
      stage('Kaniko build') {
          echo 'Kaniko is running as container entrypoint; build log is above.'
      }
  }
}
