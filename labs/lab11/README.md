# Cloud Lab 11 Submission — CI/CD with CodePipeline

Copy this template to `cc-lab-YOUR_ID/lab11/README.md` in your own repository. Follow [the instructions](lab11-instruction.md). Put your screenshots in `lab11/images/` with the file names below.

- **Student name:**
- **Student ID:**
- **Learner Lab user name:**
- **App repository:** https://github.com/YOUR_USERNAME/cicd-node-app
- **Date completed:**

---

## EC2 instance and CodeDeploy agent

![Node.js and the CodeDeploy agent](images/01-ec2-agent.png)

## Pipeline run

![Pipeline with three successful stages](images/02-pipeline-success.png)

![CodeBuild test results](images/03-codebuild-tests.png)

![CodeDeploy deployment](images/04-codedeploy-success.png)

## Website before and after the change

![Website after the first deployment](images/05-website-v1.png)

![Website after the pushed change](images/06-website-v2.png)

Link to the commit that changed the page:

---

## Questions

1. Describe what happened between your `git push` and the updated page appearing. Name each stage, the service that runs it, and the artifact it produces or uses.
2. What is the difference between `buildspec.yml` and `appspec.yml`? Which service reads each one, and where does it run?
3. The tests run during the **Build** stage. What would happen to the website if a test failed? Why is that useful?
4. How does CodeDeploy know which EC2 instance to deploy to?
5. Why did the instance need `LabInstanceProfile`?

## Problems and how I solved them (optional)

A failed pipeline run, what the logs said, and how you fixed it.

## AI note (optional)

One suggestion an AI tool gave you and how you checked it.

## Clean up

- [ ] Pipeline, CodeBuild project, CodeDeploy deployment group and application deleted.
- [ ] Instance terminated and security group deleted.
- [ ] Artifact bucket emptied and deleted.
