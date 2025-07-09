podTemplate(yaml: """
apiVersion: v1
kind: Pod
metadata:
  name: kaniko-pipeline
  namespace: jenkins
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
    - /kaniko/executor
    args:
    - --context=https://github.com/alice1989123/security_group_updater.git
    - --dockerfile=Dockerfile
    - --destination=registry.local:31504/security_group_updater:prod
    - --insecure
    - --skip-tls-verify
    - --verbosity=trace

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
        echo 'Kaniko build is already running in this container via args'
      }
    }
  }
}
