# Cloud Lab 3 Challenge Submission — Secure S3 Bucket

Copy this template to `cc-lab-YOUR_ID/lab3-challenge/README.md` in your own repository. Follow [the challenge](lab3-challenge.md). Put your screenshots in `lab3-challenge/images/` and your policy in `lab3-challenge/bucket-policy.json`.

- **Student name:**
- **Student ID:**
- **Learner Lab user name:**
- **Bucket name:**
- **Date completed:**

---

## 1. Bucket

![Bucket list](images/01-bucket.png)

## 2. Object ownership

![Object Ownership](images/02-object-ownership.png)

## 3. Public access policy

![Bucket policy](images/03a-bucket-policy.png)

![Public object loaded in the browser](images/03b-public-object.png)

![Private object denied](images/03c-private-object.png)

My policy is in [bucket-policy.json](bucket-policy.json). Explain which line limits public access to the `public/` folder:

## 4. Versioning

![Versioning enabled](images/04-versioning.png)

## 5. Lifecycle rule

![Lifecycle rule](images/05-lifecycle.png)

---

## Questions

1. You turned off parts of **Block Public Access** for this bucket. Why was that needed, and why is it still safe for the objects outside `public/`?
2. What is a **noncurrent version**? Give an example from your own test.
3. Why move noncurrent versions to S3 Standard-IA instead of deleting them?

## AI note (optional)

One suggestion an AI tool gave you and how you checked it.

## Clean up

- [ ] All object versions deleted and the bucket deleted.
