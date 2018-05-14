node {
  def project = 'sre-test-203806'
  def appName = 'birthday-app'
  def uniqueTag = "gcr.io/${project}/${appName}:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
  def latestTag = "gcr.io/${project}/${appName}:${env.BRANCH_NAME}.latest"

  checkout scm

  stage 'Build image'
  sh("docker build -t ${imageTag} .")

  stage 'Publish image'
  sh('gcloud docker -- push ${imageTag}')
  sh('gcloud container images add-tag ${imageTag} ${latestTag}')

  if (env.BRANCH_NAME == 'master') {
    // Roll out to dev environment
    stage "Deploy Rolling Dev"

    dir('deployment-config') {
        git url: 'https://github.com/kaathewise/sre-test.git' // clones config
    }
    sh('kubectl --namespace=dev apply -f deployment-config/k8s/dev/')
  }
}
