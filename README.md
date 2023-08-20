# WeatherApp
A serverless weather app deployed as a microservice using Terraform, Kubernetes, Jenkins, and Flask 
# Instructions/Assumptions:

AWS CLI, kubectl, Helm, and Terraform are installed.
AWS credentials are set up properly.
Helm 3 is being used.
The script assumes a LoadBalancer service type for Jenkins, which means you're billed for its usage. This is why an active Jenkins pipeline has not been built however, I will walk you step by step on how to create this, point it to this repo and then set up the necessary build and deploy steps. The same goes for Terraform. I am providing a sample tf that will create a simple eks cluster and walk through how to make everything go live. The code base for the items will all be in this git repo. 

# AWS Kubernetes Cluster with Jenkins CI/CD and Flask Weather Microservice

This guide provides a walkthrough of setting up a Kubernetes cluster in AWS, deploying Jenkins for continuous integration and deployment, and deploying a Flask-based microservice to display the weather for Washington, DC.

## Prerequisites

- AWS account with full admin permissions.
- AWS CLI installed and configured with the required IAM user credentials.
- Terraform installed.
- `kubectl` and `helm` installed.
- Python installed.
- A GitHub account for storing the Flask microservice's codebase. (I have hardcoded my own git repo in some steps. Please make necessary changes to point to your own repo)

## Step-by-step Guide

### 1. Infrastructure Setup using Terraform

**a.** Clone the repo and navigate to the Terraform directory.

```bash
git clone git@github.com:derekdereks/WeatherApp.git
cd WeatherApp/terraform
```
**b.** Initialize Terraform and Apply changes to create an EKS cluster in the AWS us-east-2 region.
```bash
terraform init
```
```bash
terraform apply
```
**c.**  Configure kubectl to point to the new EKS cluster.
```bash
aws eks --region us-east-2 update-kubeconfig --name weather-cluster
```
### 2. Jenkins Deployment on Kubernetes

#### a. Add the Jenkins Helm repository:

```bash
helm repo add jenkinsci https://charts.jenkins.io
helm repo update
```
#### b. Deploy Jenkins using Helm:
```bash
helm install jenkins jenkinsci/jenkins --namespace jenkins
```
#### c. Retrieve the Jenkins admin password:
```bash
printf $(kubectl get secret --namespace jenkins jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo
```
#### d. Access Jenkins using its LoadBalancer IP or domain (this might take some time to become available):
```bash
kubectl get svc --namespace jenkins jenkins
```
### 3. Flask Weather Microservice Setup

#### a. Navigate to the microservice directory:
```bash
cd WeatherApp/microservice
```
#### b. Ensure you have the required packages by installing them:
```bash
pip install -r requirements.txt
```
#### c. (optional) If any edits, Push the Flask microservice to your GitHub repository:
```bash
git init
git add .
git commit -m "Initial commit for Flask microservice"
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```
### 4. Jenkins Pipeline Configuration
#### a. Log in to the Jenkins dashboard.
#### b. Create a new pipeline job and configure its source to point to your Flask microservice GitHub repository.
#### c. Set up the build steps to:
##### -Build the Flask application.
##### -Dockerize the application.
##### -Push the Docker container to a registry (like ECR or Docker Hub).
##### -Deploy the Docker container to the EKS cluster.
###### Note: I will not be providing the steps to complete this as I do not have that much time, but as an overview you will need to create a dockerfile in the root of the flask app, install docker on Jenkins, create a docker build from a created pipeline job, then push the container to ECR or Docker Hub, and finally deploy the container to EKS by creating some form of deployment.yaml. You can add all of these steps to your Jenkins pipeline. (If this was not a requirement I would probably set up Flux to do this.)

#### d. Save and run the pipeline to automatically build and deploy the Flask microservice.

### 5. Automated Script Execution
#### a. Navigate to the automation script directory:
```bash
cd WeatherApp/script
```
#### b. Run the provided script:
```bash
python deploy.py
```
