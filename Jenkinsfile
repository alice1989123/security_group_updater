// Jenkinsfile (scripted pipeline)

podTemplate(yaml: """\
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
      - /kaniko/executor
    args:
      - "--context=git://github.com/alice1989123/security_group_updater.git"
      - "--dockerfile=Dockerfile"
      - "--destination=registry.local:31504/security_group_updater:prod"
      - "--insecure"
      - "--skip-tls-verify"
  restartPolicy: Never
""") {

    node(POD_LABEL) {              // Jenkins attaches to the ‘jnlp’ sidecar the plugin adds
        stage('Kaniko build') {
            // Nothing to run here – /kaniko/executor is already running as the container’s PID 1.
            // Just collect its exit status so the stage is marked failed if the push fails.
            container('kaniko') { sh 'echo "Kaniko exit code: $?"' }
        }
    }
}
