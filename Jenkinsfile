podTemplate(yaml: """\
apiVersion: v1
kind: Pod
metadata:
  namespace: jenkins
  name: kaniko-build
spec:
  containers:
    - name: kaniko
      image: gcr.io/kaniko-project/executor:v1.19.0   # pin a known-good tag
      command: ["/kaniko/executor"]                   # entrypoint
      args:
        - "-v=trace"                                  # log level
        - "--context=https://github.com/alice1989123/security_group_updater.git"
        - "--dockerfile=Dockerfile"
        - "--destination=registry.local:31504/security_group_updater:prod"
        - "--insecure"
        - "--skip-tls-verify"
      volumeMounts:
        - name: docker-config
          mountPath: /kaniko/.docker/
  restartPolicy: Never
  volumes:
    - name: docker-config
      secret:
        secretName: kaniko-docker-config              # `{}` is fine for an insecure registry
""") {

    node(POD_LABEL) {
        stage('Build image with Kaniko') {
            echo 'Kaniko is already running as container entrypoint; nothing to exec.'
        }
    }
}
