# ITC-I5GIC-CC — Introduction to Cloud Computing

**Institute of Technology of Cambodia** · Department of Information and Communication Engineering (GIC)

Course materials for **GICI5CC — Introduction to Cloud Computing**, academic year 2025–2026.
**Instructor:** Heng Rathpisey

## 📂 Repository Structure

```
ITC-I5GIC-CC/
├── README.md                  # ← You are here
└── labs/
    ├── SETUP.md               # AWS Academy Learner Lab, GitHub repository, how to submit
    ├── INDEX.md               # Complete lab index
    ├── REPORT-TEMPLATE.md     # Shared lab report template
    ├── lab1/                  # Lab 1 — Amazon EC2
    │   ├── lab1-instruction.md
    │   ├── README.md          #   Report template
    │   └── figures/           #   Architecture diagrams
    ├── lab2/ … lab11/         # Same layout (there is no Lab 4)
    └── lab10/files/           # CloudFormation templates and Terraform starter files
```

## 🔬 Labs

Every lab is done individually in your own **AWS Academy Learner Lab**. Start with the [student setup](labs/SETUP.md); the [lab index](labs/INDEX.md) lists every lab with its report template.

| Lab | Title | Link |
|:---:|-------|:----:|
| 1 | Amazon EC2: walkthrough and web solution challenge | [Instructions](labs/lab1/lab1-instruction.md) |
| 2 | Understanding AWS storage options (S3, EBS, EFS) | [Instructions](labs/lab2/lab2-instruction.md) · [Challenge](labs/lab2/lab2-challenge.md) |
| 3 | Amazon VPC with public and private subnets | [Instructions](labs/lab3/lab3-instruction.md) |
| 5 | Processing Amazon S3 events using AWS Lambda | [Instructions](labs/lab5/lab5-instruction.md) |
| 6 | RESTful microservices with API Gateway and DynamoDB | [Instructions](labs/lab6/lab6-instruction.md) |
| 7 | Application Load Balancer with an EC2 Auto Scaling group | [Instructions](labs/lab7/lab7-instruction.md) |
| 8 | Getting started with cost estimation | [Instructions](labs/lab8/lab8-instruction.md) |
| 9 | Getting started with Amazon ECS | [Instructions](labs/lab9/lab9-instruction.md) |
| 10 | Provisioning AWS with CloudFormation and Terraform | [Instructions](labs/lab10/lab10-instruction.md) |
| 11 | CI/CD with AWS CodePipeline | [Instructions](labs/lab11/lab11-instruction.md) |

## 🚀 Getting Started for Students

```bash
# 1. On GitHub, create an EMPTY repository named CC-GIC-<YourStudentID>

# 2. On your computer, create your course folder
$ mkdir -p ~/cc-gic-<YourStudentID>/cc-lab-<YourStudentID>
$ cd ~/cc-gic-<YourStudentID>

# 3. Initialize git and connect to your GitHub repo
$ git init
$ git branch -M main
$ git remote add origin https://github.com/<YourUsername>/CC-GIC-<YourStudentID>.git

# 4. Add the .gitignore from labs/SETUP.md, then start Lab 1
```

### 📂 Your Submission Repo Structure

```
cc-gic-<YourStudentID>/                    # GitHub repository CC-GIC-<YourStudentID>
├── .gitignore
└── cc-lab-<YourStudentID>/                # Lab submissions
    ├── lab1/
    │   ├── README.md                      # Your lab report
    │   └── images/                        # Screenshots, named as the lab lists them
    ├── lab2/
    ├── lab2-challenge/
    └── ...
```

> Each lab lists the exact files it expects. Every console screenshot must show your Learner Lab user name. Never commit keys (`*.pem`), AWS credentials or Terraform state files.

---

<div align="center">

**Introduction to Cloud Computing — ITC 2026**

</div>
