node {
  echo(message: env.JOB_NAME)
  def full_name = env.JOB_NAME.split('/')
  def directory_name = full_name[0]
  def job_name = full_name[1]
  def project = 'snsumner75'
  def appName = 'cicd-multi-service-demo'
  def feSvcName = "${appName}"
  def release = env.BRANCH_NAME.replaceAll('_','')
  def serviceType
  def replicaCount
  checkout scm

  switch (directory_name) {
     case "cicd-multi-service-demo-all-in-one":
        serviceType = 'all-in-one'
     break

     case "cicd-multi-service-demo-greeter-service":
        serviceType = 'python-greeter-service'
     break

     case "cicd-multi-service-demo-name-service":
        serviceType = 'python-name-service'
     break

     case "cicd-multi-service-demo-hello-world":
        serviceType = 'python-hello-world'
     break

     default:
     break
  }

  def imageTag = "quay.io/${project}/${appName}-${serviceType}-${env.BRANCH_NAME.toLowerCase()}:${env.BUILD_NUMBER}"

  stage('Printenv') {
     sh("printenv")
  }

  stage ('Login to Quay.io') {
     sh("docker login -u=\"${env.quay_username}\" -p=\"${env.quay_password}\" quay.io")
  }

  stage ('Build image') {
     sh("docker build -t ${imageTag} -f Dockerfile.${serviceType} .")
  }

  stage ('Push image to Quay.io registry') {
     sh("docker push ${imageTag}")
  }

  stage ("Deploy Application") {

     switch (env.BRANCH_NAME) {
        case "dev_1":
            // Roll out to DEV-INT environment
            def namespace = 'dev-int'
            replicaCount = '1'
            sh("helm upgrade ${release}-${serviceType}  charts/${serviceType}/. --install --namespace ${namespace} --reuse-values --set buildNumber=${env.BUILD_NUMBER},branch=${env.BRANCH_NAME.toLowerCase()},environment=${namespace},replicaCount=${replicaCount}")
        break

        case "rel_1":
            // Roll out to QA environment
            def namespace = 'qa'
            if (serviceType == 'all-in-one') {
               replicaCount = '1'
            } else {
               replicaCount = '3'
            }
            sh("helm upgrade ${release}-${serviceType}  charts/${serviceType}/. --install --namespace ${namespace} --reuse-values --set buildNumber=${env.BUILD_NUMBER},branch=${env.BRANCH_NAME.toLowerCase()},environment=${namespace},replicaCount=${replicaCount}")
        break

        default:
        break
     }
  }
}
