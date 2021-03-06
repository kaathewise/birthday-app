import java.text.SimpleDateFormat

node {
  def project = 'sre-test-203806'
  def appName = 'birthday-app'
  def packageName = "gcr.io/${project}/${appName}"

  checkout scm

  def commitId = sh(
    returnStdout: true,
    script: "git log -n 1 --pretty=format:'%h'").trim()
  def uniqueTag = "${packageName}:${commitId}"
  def imageExists = sh(
    returnStdout: true,
    script: "gcloud container images list-tags ${packageName} | grep ${commitId} | wc -l"
  ).trim()

  if (imageExists == '0') {
    stage 'Build image'
    sh("docker build -t ${uniqueTag} .")

    stage 'Publish image'
    sh("gcloud docker -- push ${uniqueTag}")
  }

  def latestTag = "${packageName}:latest"
  def liveTag = "${packageName}:live"
  def RCTag = "${packageName}:RC${new SimpleDateFormat("yyyyMMdd_HHmm").format(new Date())}"

  switch (env.BRANCH_NAME) {
    case 'master':
      stage "Update latest tag"
      sh("gcloud container images add-tag ${uniqueTag} ${latestTag}")

      stage "Deploy rolling dev"
      sh("kubectl --namespace=dev set image deployment/birthday-app-dev backend=${uniqueTag}")
      break;

    case 'release':
      stage "Update RCxx tag"
      sh("gcloud container images add-tag ${uniqueTag} ${RCTag}")

      stage "Deploy Prod"
      sh("kubectl --namespace=prod set image deployment/birthday-app backend=${uniqueTag}")

      stage "Update live tag"
      sh("gcloud container images add-tag ${uniqueTag} ${liveTag}")
      break;
  }
}
