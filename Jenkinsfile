node {
  def project = 'snsumner75'
  def appName = 'cicd-multi-service-demo'
  def feSvcName = "${appName}"
  def release = env.BRANCH_NAME.replaceAll('_','')
  checkout scm

  if (env.JOB_NAME.contains('cicd-multi-service-demo-all-in-one')) {
     def serviceType = 'all-in-one'
  }

  if (env.JOB_NAME.contains('cicd-multi-service-demo-greeter-service')) {
     def serviceType = 'greeter-service'
  }

  if (env.JOB_NAME.contains('cicd-multi-service-demo-name-service')) {
     def serviceType = 'name-service'
  }

  if (env.JOB_NAME.contains('cicd-multi-service-demo-hello-world')) {
     def serviceType = 'hello-world'
  }

  def imageTag = "quay.io/${project}/${appName}-${env.serviceType}-${env.BRANCH_NAME.toLowerCase()}:${env.BUILD_NUMBER}"

  stage('Printenv') {
     sh("printenv")
  }


  stage ('Login to Quay.io') {
     sh("docker login -u=\"${env.quay_username}\" -p=\"${env.quay_password}\" quay.io")
  }

  stage ('Build image') {

    switch ("${serviceType}") {
       case "all-in-one":
         sh("docker build -t ${imageTag} -f Dockerfile.all-in-one .")
       break

       case "greeter-service":
         sh("docker build -t ${imageTag} -f Dockerfile.python-greeter-service .")
       break

       case "name-service":
         sh("docker build -t ${imageTag} -f Dockerfile.python-name-service .")
       break

       case "hello-world":
         sh("docker build -t ${imageTag} -f Dockerfile.python-hello-world .")
       break

       default:
       break
    }
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
