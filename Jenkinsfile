import java.text.SimpleDateFormat

node {
  def project = 'sre-test-203806'
  def appName = 'birthday-app'
  def package = "gcr.io/${project}/${appName}"
  def uniqueTag = "${package}:${env.GIT_COMMIT}"
  def latestTag = "${package}:latest"
  def liveTag = "${package}:live"
  def RCTag = "${package}:RC${new SimpleDateFormat("yyyyMMddHHmm").format(new Date())}"

  checkout scm

  stage 'Build image'
  sh("docker build -t ${uniqueTag} .")

  stage 'Publish image'
  sh("gcloud docker -- push ${uniqueTag}")

  switch (env.BRANCH_NAME) {
    case 'master':
      stage "Update 'latest' tag"
      sh("gcloud container images add-tag ${uniqueTag} ${latestTag}")

      stage "Deploy Rolling Dev"
      sh("kubectl --namespace=dev set image deployment/birthday-app-dev backend=${uniqueTag}")

    case 'release':
      stage "Update RCxx tag"
      sh("gcloud container images add-tag ${uniqueTag} ${RCTag}")

      stage "Deploy Prod"
      sh("kubectl --namespace=dev set image deployment/birthday-app-dev backend=${uniqueTag}")

      stage "Update 'live' tag"
      sh("gcloud container images add-tag ${uniqueTag} ${liveTag}")
  }
}
