# Cloud Lab 9 Submission — Amazon ECS

Copy this template to `cc-lab-YOUR_ID/lab9/README.md` in your own repository. Follow [the instructions](lab9-instruction.md). Put your screenshots in `lab9/images/` and your application files in `lab9/app/`.

- **Student name:**
- **Student ID:**
- **Learner Lab user name:**
- **Build environment used:** Cloud9 / EC2 instance
- **Date completed:**

---

## 1. Image in ECR

![ECR repository with the latest image](images/01-ecr-image.png)

## 2. Target group health

![Two healthy targets](images/02-target-health.png)

## 3. ECS service

![ecs-demo-service with 2 running tasks](images/03-ecs-service.png)

## 4. Load balancer

![ecs-demo-alb details](images/04-load-balancer.png)

## 5–6. Application in two Availability Zones

![Zone us-east-1a](images/05-app-zone-a.png)

![Zone us-east-1b](images/06-app-zone-b.png)

## Application files

- [app/app.py](app/app.py)
- [app/Dockerfile](app/Dockerfile)

---

## Questions

1. Put these in the order they happen and say what each does: `docker push`, `docker build`, `docker login`, `docker tag`.
2. What is the difference between the ECR **repository**, the ECS **task definition**, a **task** and the ECS **service**?
3. `ecs-task-sg` allows port 5000 only from `alb-sg`. What would happen if you opened `http://<task-public-IP>:5000` directly in your browser? Why is this rule safer than allowing port 5000 from anywhere?
4. Why must the target group use the target type **IP addresses** for Fargate tasks?
5. Stop one of the two tasks in the console (optional). What does the service do, and why?

## Problems and how I solved them (optional)

## AI note (optional)

One suggestion an AI tool gave you and how you checked it.

## Clean up

- [ ] ECS service and cluster deleted.
- [ ] Load balancer and target group deleted.
- [ ] Cloud9 environment (or EC2 build instance) deleted.
- [ ] ECR repository deleted.
- [ ] Security groups `ecs-task-sg` and `alb-sg` deleted.
