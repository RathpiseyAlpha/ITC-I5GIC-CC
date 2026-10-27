# Cloud Lab index

GICI5CC — Introduction to Cloud Computing · Institute of Technology of Cambodia, Department GIC

Start with the [student setup](SETUP.md): it explains the AWS Academy Learner Lab, how to create your GitHub repository `CC-GIC-YOUR_ID`, and how to submit. Every lab has an instruction file and a report template (`README.md`) that you copy into your repository. The [general report template](REPORT-TEMPLATE.md) shows the shape all reports follow.

| Lab | Title | Services | Student files | Screenshots |
|---|---|---|---|:---:|
| 1 | Amazon EC2: walkthrough and web solution challenge | EC2, security groups, key pairs | [Instruction](lab1/lab1-instruction.md) · [Report](lab1/README.md) | 10 |
| 2 | Application Load Balancer with an EC2 Auto Scaling group | ELB, EC2 Auto Scaling | [Instruction](lab2/lab2-instruction.md) · [Report](lab2/README.md) | 14 |
| 3 | Understanding AWS storage options | S3, EBS, EFS | [Instruction](lab3/lab3-instruction.md) · [Report](lab3/README.md) | 9 |
| 3 (challenge) | Secure and manage an S3 bucket for public content | S3 policies, versioning, lifecycle | [Instruction](lab3/lab3-challenge.md) · [Report](lab3/challenge-README.md) | 6 (+1) |
| 4 | Amazon VPC with public and private subnets | VPC, internet gateway, NAT gateway, Systems Manager | [Instruction](lab4/lab4-instruction.md) · [Report](lab4/README.md) | 11 |
| 5 | Processing Amazon S3 events using AWS Lambda | Lambda, S3, CloudWatch | [Instruction](lab5/lab5-instruction.md) · [Report](lab5/README.md) | 2 |
| 6 | RESTful microservices with API Gateway and DynamoDB | API Gateway, DynamoDB, CloudShell | [Instruction](lab6/lab6-instruction.md) · [Report](lab6/README.md) | 7 |
| 8 | Getting started with cost estimation | AWS Pricing Calculator | [Instruction](lab8/lab8-instruction.md) · [Report](lab8/README.md) | 6 |
| 9 | Getting started with Amazon ECS | ECR, ECS on Fargate, ALB, Cloud9 | [Instruction](lab9/lab9-instruction.md) · [Report](lab9/README.md) | 6 |
| 10 | Provisioning AWS with infrastructure as code | CloudFormation, Terraform | [Instruction](lab10/lab10-instruction.md) · [Report](lab10/README.md) | 16 |
| 11 | CI/CD with AWS CodePipeline | CodePipeline, CodeBuild, CodeDeploy, GitHub | [Instruction](lab11/lab11-instruction.md) · [Report](lab11/README.md) | 6 |

There is no Lab 7. Lab numbers match the lab documents used in class.

## Submission at a glance

```text
GitHub repository: CC-GIC-YOUR_ID
cc-gic-YOUR_ID/
├── .gitignore
└── cc-lab-YOUR_ID/
    ├── lab1/
    │   ├── README.md          # report, from the lab's template
    │   └── images/            # screenshots, named as the lab lists them
    ├── lab2/
    ├── lab3/
    ├── lab3-challenge/
    ├── lab4/
    ├── lab5/ … lab11/
```

- One folder per lab, named exactly `labN` (and `lab3-challenge`).
- Screenshots in `images/`, PNG, with the file names the lab gives. Every console screenshot shows your Learner Lab user name.
- Commit message: `Lab N: <short description>`.
- Never commit keys (`*.pem`), AWS credentials, or Terraform state files.
