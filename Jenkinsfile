node {
  def project = 'sre-test'
  def appName = 'birthday-app'
  def imageTag = "gcr.io/${project}/${appName}:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"

  checkout scm

  stage 'Build image'
  sh("docker build -t ${imageTag} .")

  stage 'Publish image'
  environment {
    GOOGLE_APPLICATION_CREDENTIALS = credentials('sre-test-203806')
  }
  sh("gcloud docker -- push ${imageTag}")
}
