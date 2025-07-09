podTemplate(yaml: """\
apiVersion: v1
kind: Pod
metadata:
  name: kaniko-pipeline
  namespace: jenkins
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:v1.19.0  # a known-good tag
    command:
      - /busybox/sh
      - -c
    args:
      - "while true; do sleep 3600; done"
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
                    --verbosity=trace \
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
