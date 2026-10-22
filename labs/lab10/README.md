# Cloud Lab 10 Submission — Infrastructure as Code

Copy this template to `cc-lab-YOUR_ID/lab10/README.md` in your own repository. Follow [the instructions](lab10-instruction.md). Put your screenshots in `lab10/images/`, the CloudFormation templates in `lab10/cloudformation/` and your Terraform code in `lab10/terraform/`.

- **Student name:**
- **Student ID:**
- **Learner Lab user name:**
- **Where I ran Terraform** (Windows/WSL/macOS/Linux, Terraform version):
- **Date completed:**

---

## Part 10.1 — AWS CloudFormation

### Stack created

![Stack resources](images/01-cf-resources.png)

![Stack outputs](images/02-cf-outputs.png)

![First instance in the browser](images/03-cf-browser.png)

### Stack updated

![Resources after the update](images/04-cf-updated-resources.png)

![Outputs after the update](images/05-cf-updated-outputs.png)

![Second instance in the browser](images/06-cf-second-browser.png)

Templates: [original](cloudformation/CloudFormation_Lab_Template.yaml) · [updated](cloudformation/CloudFormation_Lab_Updated_Template.yaml)

---

## Part 10.2 — Terraform

### S3 bucket, object and policy

![terraform apply: bucket](images/07-tf-s3-apply.png)

![terraform apply: index.html](images/08-tf-object-apply.png)

![index.html in the bucket](images/09-tf-s3-ls.png)

![Bucket policy](images/10-tf-bucket-policy.png)

### Lambda function and function URL

![terraform apply: Lambda](images/11-tf-lambda-apply.png)

![function_url output](images/12-tf-function-url.png)

![Function URL in the browser](images/13-tf-function-url-browser.png)

### EC2 instance

![Security group port 3000](images/14-tf-security-group.png)

![public_ip output](images/15-tf-public-ip.png)

![React app](images/16-tf-react-app.png)

My Terraform code: [main.tf](terraform/main.tf) · [lambda.py](terraform/lambda.py) · [index.html](terraform/index.html)

---

## Questions

1. In the CloudFormation **Changeset preview** of the update, which resources were added, and was the first instance changed or replaced? How can you tell?
2. To remove everything in Part 10.1 you deleted one stack. What is the advantage compared with deleting each resource in the console?
3. Why did you run `terraform init` again before creating the Lambda function?
4. What is stored in `terraform.tfstate`, and why must it **not** be committed to Git?
5. The `aws_s3_bucket_acl` block has a `depends_on`. What would go wrong without it?
6. Compare CloudFormation and Terraform: name one thing they have in common and one difference you noticed in this lab.

## Problems and how I solved them (optional)

## AI note (optional)

One suggestion an AI tool gave you and how you checked it.

## Clean up

- [ ] Stack `cf-lab-stack` deleted.
- [ ] `terraform destroy` finished with *Destroy complete*.
