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
  checkout scm

  echo(message: directory_name)

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

  echo(message: serviceType)

  def imageTag = "quay.io/${project}/${appName}-${serviceType}-${env.BRANCH_NAME.toLowerCase()}:${env.BUILD_NUMBER}"

  echo(message: imageTag)

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
            sh("helm upgrade ${release}-${serviceType}  charts/all-in-one/. --install --namespace ${namespace} --reuse-values --set buildNumber=${env.BUILD_NUMBER},branch=${env.BRANCH_NAME.toLowerCase()},environment=${namespace},replicaCount=1")
        break

        case "rel_1":
            // Roll out to QA environment
            def namespace = 'qa'
            sh("helm upgrade ${release} charts/. --install --namespace ${namespace} --reuse-values --set buildNumber=${env.BUILD_NUMBER},branch=${env.BRANCH_NAME.toLowerCase()},environment=${namespace},replicaCount=4")
        break

        default:
        break
     }
  }
}
