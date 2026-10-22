# Cloud Lab 8 Submission — Cost Estimation

Copy this template to `cc-lab-YOUR_ID/lab8/README.md` in your own repository. Follow [the instructions](lab8-instruction.md). Put your screenshots in `lab8/images/` and your CSV export in `lab8/estimate.csv`.

- **Student name:**
- **Student ID:**
- **Date completed:**
- **Public estimate link:** <paste the link from the Share dialog here>
- **CSV export:** [estimate.csv](estimate.csv)

---

## 1. Services added

![My Estimate with three services](images/01-services-added.png)

## 2. Load balancer configuration

![Elastic Load Balancing configuration](images/02-load-balancer.png)

## 3. EC2 configuration

![EC2 configuration](images/03-ec2.png)

## 4. Cost summary

![Estimate summary](images/04-summary.png)

| Service | Monthly cost (USD) | 12-month cost (USD) |
|---|---:|---:|
| Elastic Load Balancing | | |
| Amazon EC2 | | |
| Amazon RDS for MySQL | | |
| **Total** | | |

## 5. CSV export

![CSV export](images/05-csv-export.png)

## 6. Shared link

![Share dialog](images/06-share-link.png)

---

## Questions

1. Which service costs the most in your estimate? Give one reason from its configuration.
2. Change the RDS deployment from **Multi-AZ** to **Single-AZ** (do not save it in your shared estimate). How does the RDS cost change, and what do you lose by choosing Single-AZ?
3. The EC2 workload uses **Daily spike traffic** (1 instance, 2 at peak). Why is this cheaper than running 2 instances all the time?
4. Why is it useful to estimate the cost of an architecture **before** deploying it?

## AI note (optional)

One suggestion an AI tool gave you and how you checked it.
