provider "aws" {
  region = "us-east-2"
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "my-cluster"
  cluster_version = "1.21"
  subnets         = ["subnet-abcde012", "subnet-bcde012a"]

  node_groups = {
    eks_nodes = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1
      key_name         = var.key_name
    }
  }
}
