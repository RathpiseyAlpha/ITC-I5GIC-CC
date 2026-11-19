# Cloud Lab 7 Submission — AWS Databases

Copy this template to `cc-lab-YOUR_ID/lab7/README.md` in your student repository. Follow [the lab instructions](lab7-instruction.md) and save your screenshots in `lab7/images/`.

- **Student name:**
- **Student ID:**
- **Region:**

## Lab evidence

![EC2 security group and SSH rule](images/01-security-group.png)

![Running EC2 instance](images/02-ec2-running.png)

![Private S3 media bucket](images/03-s3-media-bucket.png)

![RDS MySQL instance and endpoint](images/04-rds-mysql.png)

![Aurora writer and reader endpoints](images/05-aurora-endpoints.png)

![DynamoDB table and partition key](images/06-dynamodb-table.png)

![App starting on EC2](images/07-app-start.png)

![Demo post and image in the browser](images/08-app-post.png)

![Matching DynamoDB item](images/09-post-item.png)

## Trace one post

| Where | What you found |
|---|---|
| RDS `user_post` | Post ID and demo username |
| DynamoDB `posts` | Matching `post_id`, title and `media_key` |
| S3 | Object key matching `media_key` |

1. Which database does signup write to, and which Aurora endpoint does login use? Explain what the reader endpoint does when there is only one instance.
2. Why does the app use the same ID in RDS and DynamoDB? What would happen if one of the two writes failed after the other succeeded?
3. Explain how your browser can display an image even though the S3 bucket blocks public access.

## Cleanup

- [ ] EC2 instance terminated and lab security groups removed.
- [ ] RDS instance and Aurora cluster deleted.
- [ ] S3 bucket emptied and deleted.
- [ ] DynamoDB table deleted.
