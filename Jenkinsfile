podTemplate(yaml: """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    # default ENTRYPOINT = /kaniko/executor
    args:
      - --context=git://github.com/alice1989123/security_group_updater.git
      - --dockerfile=Dockerfile
      - --destination=registry.local:31504/security_group_updater:prod2
      - --insecure
      - --skip-tls-verify
""") {

  node(POD_LABEL) {
    stage('Build') {
      /* Nothing to run here – kaniko finishes, pod exits 0,
         Jenkins marks the step SUCCESS                         */
    }
  }
}
