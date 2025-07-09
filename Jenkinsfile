podTemplate(yaml: """\
apiVersion: v1
kind: Pod
spec:
  volumes:
    - name: kaniko-out
      persistentVolumeClaim:
        claimName: kaniko-output
  containers:
    - name: kaniko
      image: gcr.io/kaniko-project/executor:latest
      command: ["/kaniko/executor"]
      args:
        - "-v=info"
        - "--context=git://github.com/alice1989123/security_group_updater.git"
        - "--dockerfile=Dockerfile"
        - "--tar-path=/kaniko-out/sgu.tar"   # write here
        - "--no-push"
      volumeMounts:
        - name: kaniko-out
          mountPath: /kaniko-out
    - name: jnlp
      image: jenkins/inbound-agent:3309.v27b_9314fd1a_4-1
      volumeMounts:
        - name: kaniko-out
          mountPath: /kaniko-out
  restartPolicy: Never
""") {

  node(POD_LABEL) {
    stage('Kaniko build (tar only)') {
      echo 'Kaniko is building and saving /kaniko-out/sgu.tar …'
    }

    stage('Show tar') {
      sh 'ls -lh /kaniko-out'
    }

    /* optional: publish so you can download from the Jenkins UI */
    archiveArtifacts artifacts: 'kaniko-out/sgu.tar', fingerprint: true
  }
}
