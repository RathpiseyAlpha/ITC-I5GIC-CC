# Cloud Lab 7 — Build a Social App with AWS Databases (Hands-on)

| | |
|---|---|
| Environment | AWS Academy Learner Lab, US East (N. Virginia) `us-east-1` |
| Technologies | Amazon EC2, RDS for MySQL, Aurora MySQL, DynamoDB, S3 |
| Submit | `cc-lab-YOUR_ID/lab7/README.md` and 9 screenshots in `lab7/images/` |

Deploy a small social app on EC2. Sign up and sign in, publish a post, and trace the same post across two databases and an optional image in S3. The exercise is adapted from Educative's [DatabaseOptions lab](https://github.com/Educative-Content/DatabaseOptions). This version includes its own [starter app](files/app.py).

```text
Your browser ── SSH tunnel ── EC2 app
                               ├── Aurora MySQL  users and password hashes
                               ├── RDS MySQL     post IDs and authors
                               ├── DynamoDB      post titles, text and media keys
                               └── S3            private image objects
```

Read the [student setup](../SETUP.md) first. Use a made-up email (such as `student@example.com`), a throwaway password, and a small test image you can share. Finish the cleanup in the same session because the databases consume your Learner Lab budget while running.

## Screenshots to submit

Keep your Learner Lab user name visible in each console screenshot. Keep the command visible in the terminal screenshot and the address bar visible in the browser screenshot. Keep passwords, keys and signed S3 URLs out of your report and screenshots.

| File | What to show |
|---|---|
| `01-security-group.png` | The EC2 security group and its SSH inbound rule |
| `02-ec2-running.png` | The running instance with its security group |
| `03-s3-media-bucket.png` | Your bucket's Permissions tab with Block Public Access enabled |
| `04-rds-mysql.png` | The available RDS for MySQL instance and its endpoint |
| `05-aurora-endpoints.png` | The available Aurora cluster's writer and reader endpoints |
| `06-dynamodb-table.png` | The active `posts` table with the String partition key `post_id` |
| `07-app-start.png` | The command starting the app on EC2 and its listening address |
| `08-app-post.png` | The app at `http://127.0.0.1:8000/` with your demo post, image and post ID |
| `09-post-item.png` | The matching DynamoDB item with the same `post_id` and `media_key` |

## 1. Launch the EC2 host

1. In **EC2 → Security Groups**, create `aws-database-options-security-group` in the default VPC. Allow inbound **SSH (TCP 22)** from **My IP**. Keep the default outbound rules. Capture `01-security-group.png`.
2. Launch `aws-database-options-lab-instance` in the same VPC. Use Ubuntu Server 24.04 LTS (64-bit x86), `t2.micro` if available in your Learner Lab, and an 8 GiB `gp3` root volume. Enable a public IPv4 address for SSH and select the group you just created.
3. Select or create a key pair you can use from your computer. Under **Advanced details → IAM instance profile**, select `LabInstanceProfile` so the app can call DynamoDB and S3 with the instance's temporary credentials.
4. Wait for the instance to run and capture `02-ec2-running.png`. In the following command, substitute your key path and instance's public IPv4 address. Run it on your own computer and keep the connection open while testing the app.

   ```bash
   ssh -i ~/path/to/your-key.pem -L 127.0.0.1:8000:127.0.0.1:8000 ubuntu@YOUR_EC2_PUBLIC_IP
   ```

   The browser will reach the app through SSH. Leave port 8000 closed in the EC2 security group. See [AWS guidance on connecting to EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect.html) if SSH fails.

## 2. Create the private media bucket and DynamoDB table

1. In **S3 → Create bucket**, create a general-purpose bucket named `clab-imagestore-YOUR_UNIQUE_SUFFIX` in `us-east-1`. Replace the suffix with a unique lowercase value. Keep **Block all public access** and the default encryption enabled. Capture `03-s3-media-bucket.png`.
2. In **DynamoDB → Tables → Create table**, use the name `posts`, with `post_id` as the **String** partition key. Leave the sort key empty and use on-demand capacity. Wait for **Active** and capture `06-dynamodb-table.png`.

## 3. Create the two MySQL databases

Open **RDS → Databases → Create database** and use **Standard create** for each database.

| Setting | RDS for MySQL | Aurora MySQL |
|---|---|---|
| Engine | MySQL 8.0, choosing a version offered in the console | Aurora (MySQL Compatible), choosing a version offered in the console |
| Identifier | `aws-dbo-sql` | `aws-dbo-aurora` |
| Template | Dev/Test, if shown | Dev/Test, if shown |
| Deployment | Single DB instance | One writer and no Aurora Replica |
| Instance class | `db.t3.small` or the smallest class your Learner Lab permits | `db.t3.medium` or the smallest provisioned class your Learner Lab permits |
| Storage | `gp3` at the console minimum or the storage option required by your Learner Lab | Aurora Standard, if shown |
| Master username | `admin` | `admin` |
| Initial database name | `educative_db` under Additional configuration | `educative_db` under Additional configuration |

For each database, use self-managed credentials and set a distinct lab password. Under **Connectivity**, select **Connect to an EC2 compute resource** and choose your EC2 instance. Keep public access off. If you need to configure the connection manually, use the same VPC and allow MySQL (TCP 3306) into the database security group only from the EC2 security group. When the resources are available, record the RDS endpoint and the Aurora writer and reader endpoints. Capture `04-rds-mysql.png` and `05-aurora-endpoints.png`.

If a required instance class or database action is blocked, check the Learner Lab settings with your instructor before creating a larger instance. The [RDS connection guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/ec2-rds-connect.html) and [Aurora setup guide](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_GettingStartedAurora.CreatingConnecting.Aurora.html) show the console options.

## 4. Create the SQL tables from EC2

In the SSH session on EC2, install the MySQL client and download the AWS certificate bundle for `us-east-1`.

```bash
sudo apt-get update
sudo apt-get install -y mysql-client python3-venv git curl
curl -fsSLo "$HOME/rds-us-east-1.pem" \
  https://truststore.pki.rds.amazonaws.com/us-east-1/us-east-1-bundle.pem
export LAB_RDS_CA="$HOME/rds-us-east-1.pem"
export LAB_RDS_HOST='YOUR_RDS_ENDPOINT'
export LAB_AURORA_WRITER='YOUR_AURORA_WRITER_ENDPOINT'
export LAB_AURORA_READER='YOUR_AURORA_READER_ENDPOINT'
```

Use the endpoint hostnames without `https://` or `:3306`. Connect to RDS MySQL, enter its password at the prompt, and create the post index table.

```bash
mysql -h "$LAB_RDS_HOST" -u admin -p --ssl-mode=VERIFY_IDENTITY --ssl-ca="$LAB_RDS_CA" educative_db
```

```sql
CREATE TABLE IF NOT EXISTS user_post (
    id CHAR(32) PRIMARY KEY,
    username VARCHAR(80) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
EXIT;
```

Connect to the Aurora **writer** endpoint with the Aurora password and create the users table.

```bash
mysql -h "$LAB_AURORA_WRITER" -u admin -p --ssl-mode=VERIFY_IDENTITY --ssl-ca="$LAB_RDS_CA" educative_db
```

```sql
CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(254) PRIMARY KEY,
    username VARCHAR(80) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);
EXIT;
```

The app uses the writer for signup and the reader endpoint for login. With only one Aurora instance, both endpoints reach the same instance. See [Aurora reader endpoints](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Endpoints.Reader.html).

## 5. Run the app and trace one post

On EC2, clone the course repository. Install the starter app's dependencies in a virtual environment.

```bash
git clone https://github.com/RathpiseyAlpha/ITC-I5GIC-CC.git
cd ITC-I5GIC-CC/labs/lab7/files
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In the same SSH shell, enter the database passwords at the hidden prompts and start the app. Change the bucket name to yours. If you start a new shell, set the endpoint and certificate variables from Step 4 again.

```bash
export AWS_REGION=us-east-1
export LAB_MEDIA_BUCKET='clab-imagestore-YOUR_UNIQUE_SUFFIX'
export LAB_SESSION_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
read -rsp 'RDS MySQL password: ' LAB_RDS_PASSWORD; printf '\n'
read -rsp 'Aurora password: ' LAB_AURORA_PASSWORD; printf '\n'
export LAB_RDS_PASSWORD LAB_AURORA_PASSWORD
python app.py
```

1. Capture `07-app-start.png`. Browse to `http://127.0.0.1:8000/` on the computer where you opened the SSH tunnel.
2. Create a demo account and sign in. Write a post with a PNG or JPEG under 2 MiB. Confirm that it appears with its image and post ID, then capture `08-app-post.png`.
3. In DynamoDB, open **Explore table items** for `posts`. Locate your post ID and capture `09-post-item.png`. Verify that the `media_key` matches an object in the S3 bucket under `posts/`.
4. In a second SSH session, connect to RDS MySQL with the command from Step 4 after setting the endpoint and certificate variables there. Query `SELECT id, username FROM user_post;` and verify that the row has the same ID. Record the matching ID and object key in your report.

If a MySQL connection times out, check the VPC and inbound rule on the database security group. If an upload or query returns `AccessDenied`, check the EC2 instance profile and the Learner Lab permissions. The app uses [short-lived signed S3 URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html) to display images from the private bucket.

## 6. Clean up

After capturing the evidence, stop the app with `Ctrl+C` and terminate the EC2 instance. Delete the RDS instance and the Aurora cluster with its writer instance. For these disposable lab databases, skip final snapshots and remove retained backups if prompted. Empty and delete the S3 bucket, delete the DynamoDB table, and remove the lab security groups once no resource uses them. Check the RDS console again after the deletions finish.

## 7. Submit

Copy the [report template](README.md) to `cc-lab-YOUR_ID/lab7/README.md`, fill it in, and put the nine PNGs in `cc-lab-YOUR_ID/lab7/images/`. From the root of your **student** repository, run:

```bash
git add cc-lab-YOUR_ID/lab7
git commit -m "Lab 7: AWS databases"
git push
```

Open Lab 7 in your GitHub repository and verify that all nine images render.
