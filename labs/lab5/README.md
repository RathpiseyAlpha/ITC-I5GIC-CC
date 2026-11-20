# Cloud Lab 5 Submission — AWS Database Lab

Copy this template to `cc-lab-YOUR_ID/lab5/README.md` in your student repository. Follow [the lab instructions](lab5-instruction.md) and save your screenshots in `lab5/images/` with the file names below. This report is the single document that holds all your screenshots. Each heading labels the screenshot under it.

- **Student name:**
- **Student ID:**
- **Learner Lab user name:**
- **Date completed:**

Make sure resource names, statuses and endpoints are readable in every screenshot. Never show your database passwords or the AWS access key, secret key or session token.

---

## 1. Security Group Rules

`aws-database-options-security-group` with its inbound rules (SSH port 22, Custom TCP ports 8000 and 5173) and its outbound rule.

![Security group rules](images/01-security-group.png)

## 2. EC2 Instance Running

`aws-database-options-lab-instance` in the **Running** state with `aws-database-options-security-group` attached.

![EC2 instance running](images/02-ec2-running.png)

## 3. S3 Bucket

Your `clab-imagestore-…` bucket with its public access settings and bucket policy visible.

![S3 bucket permissions](images/03-s3-bucket.png)

## 4. RDS DB Instance

`aws-dbo-sql` with the status **Available** and its endpoint visible.

![RDS DB instance](images/04-rds-sql.png)

## 5. Aurora DB Status

The `aws-dbo-aurora` cluster with the status **Available** and its writer and reader endpoints visible.

![Aurora DB status](images/05-aurora-cluster.png)

## 6. DynamoDB Table

The `posts` table with the status **Active** and its partition key `post_id` visible.

![DynamoDB table](images/06-dynamodb-table.png)

## 7. Application Configuration and Testing

The EC2 instance terminal after `npm start`, showing that the application started.

![Application started in the terminal](images/07-app-start.png)

The application running in your browser at `http://<Public_IP_of_EC2>:5173`, with the address bar visible.

![Application in the browser](images/08-app-browser.png)

Optional: the signup or login page and a sample post. Delete the image line below if you did not take this screenshot.

![Signup and sample post](images/10-signup-post.png)

## 8. Final Infrastructure

One collage of the resources you created: EC2 instance, security group, RDS and Aurora databases, DynamoDB table and S3 bucket.

![Final infrastructure](images/09-final-infrastructure.png)

## Errors and troubleshooting (optional)

Screenshots of any error messages you met, and what you did about them.

---

## Questions

1. Signup writes to the Aurora **writer** endpoint and login reads from the **reader** endpoint. Your cluster has no Aurora Replica. Which instance answers the reader endpoint, and why does the application still work?
2. A post is split between the `user_post` table in RDS and the `posts` table in DynamoDB. What does each one store, and how does `/get_posts` join them?
3. The post ID is the username followed by the time (`%H:%M:%S`). What happens if the same user publishes two posts in the same second, or on two different days at the same time?
4. Why does the post content go into DynamoDB instead of a SQL table, according to the lab's database design?
5. The `users` table stores the password exactly as the user typed it, and the S3 bucket allows anyone to read its objects. Name one risk of each choice.

## Clean up

- [ ] EC2 instance terminated and `aws-database-options-security-group` deleted.
- [ ] RDS instance `aws-dbo-sql` and Aurora cluster `aws-dbo-aurora` deleted.
- [ ] S3 bucket emptied and deleted.
- [ ] DynamoDB table `posts` deleted.
