import os
import subprocess
import time


def run_terraform():
    os.chdir("path_to_terraform_directory")  # path to your Terraform directory
    subprocess.run(["terraform", "init"])
    subprocess.run(["terraform", "apply", "-auto-approve"])


def install_jenkins():
    subprocess.run(["helm", "repo", "add", "jenkins", "https://charts.jenkins.io"])
    subprocess.run(["helm", "repo", "update"])
    subprocess.run(
        [
            "helm",
            "install",
            "jenkins",
            "jenkins/jenkins",
            "--set",
            "master.serviceType=LoadBalancer",
        ]
    )
    time.sleep(60)  # Give Jenkins time to start up


def get_jenkins_url():
    result = subprocess.run(
        [
            "kubectl",
            "get",
            "svc",
            "jenkins",
            "-o",
            "jsonpath='{.status.loadBalancer.ingress[0].hostname}'",
        ],
        capture_output=True,
    )
    return result.stdout.decode().strip("'")


if __name__ == "__main__":
    run_terraform()
    install_jenkins()
    print(f"Jenkins should be available at: {get_jenkins_url()}")
    print("Please set up the Jenkins pipeline manually for the microservice.")
