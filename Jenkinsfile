import java.text.SimpleDateFormat

node {
  def project = 'sre-test-203806'
  def appName = 'birthday-app'
  def packageName = "gcr.io/${project}/${appName}"

  checkout scm

  def commitId = sh(returnStdout: true, script: "git log -n 1 --pretty=format:'%H'").trim()
  def uniqueTag = "${packageName}:${commitId}"
  def latestTag = "${packageName}:latest"
  def liveTag = "${packageName}:live"
  def RCTag = "${packageName}:RC${new SimpleDateFormat("yyyyMMddHHmm").format(new Date())}"

  stage 'Build image' {
    sh("docker build -t ${uniqueTag} .")
  }

  stage 'Publish image' {
    sh("gcloud docker -- push ${uniqueTag}")
  }

  switch (env.BRANCH_NAME) {
    case 'master':
      stage "Update 'latest' tag" {
        sh("gcloud container images add-tag ${uniqueTag} ${latestTag}")
      }
      stage "Deploy Rolling Dev" {
        sh("kubectl --namespace=dev set image deployment/birthday-app-dev backend=${uniqueTag}")
      }
      break;
    case 'release':
      stage "Update RCxx tag" {
        sh("gcloud container images add-tag ${uniqueTag} ${RCTag}")
      }
      stage "Deploy Prod" {
        sh("kubectl --namespace=dev set image deployment/birthday-app-dev backend=${uniqueTag}")
      }
      stage "Update 'live' tag" {
        sh("gcloud container images add-tag ${uniqueTag} ${liveTag}")
      }
      break;
  }
}
