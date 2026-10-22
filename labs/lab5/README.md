# Cloud Lab 5 Submission — S3 Events with AWS Lambda

Copy this template to `cc-lab-YOUR_ID/lab5/README.md` in your own repository. Follow [the instructions](lab5-instruction.md). Put your screenshots in `lab5/images/` and your function code in `lab5/lambda_function.py`.

- **Student name:**
- **Student ID:**
- **Learner Lab user name:**
- **Bucket name:**
- **Date completed:**

---

## Files sorted by type

![Uploaded file moved into its type folder](images/01-s3-organized.png)

Which files did you upload, and which folders did the function create?

## CloudWatch logs

![CloudWatch log events](images/02-cloudwatch-logs.png)

## Function code

My function code is in [lambda_function.py](lambda_function.py).

---

## Questions

1. Describe, step by step, what happens from the moment you click **Upload** until the log line appears in CloudWatch. Name each AWS service involved.
2. Why was the trigger limited to **PUT** events? What would happen with **All object create events**?
3. The function uses `LabRole`. Which two permissions does this role need for the function to work?
4. You never started or stopped a server in this lab. Who runs your code, and what do you pay for?

## Problems and how I solved them (optional)

## AI note (optional)

One suggestion an AI tool gave you and how you checked it.

## Clean up

- [ ] Lambda function deleted.
- [ ] S3 bucket emptied and deleted.
