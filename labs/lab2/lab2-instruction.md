# Cloud Lab 2 — Attach an Application Load Balancer to an EC2 Auto Scaling Group (Hands-on)

| Item | Details |
|---|---|
| Work | Individual, in your own AWS Academy Learner Lab |
| Region | US East (N. Virginia) `us-east-1` |
| Technologies | Elastic Load Balancing (Application Load Balancer), Amazon EC2 Auto Scaling, Amazon EC2 |
| Submit | `cc-lab-YOUR_ID/lab2/` in your GitHub repository `CC-GIC-YOUR_ID`: `README.md` and 14 screenshots |

> **Overview:** Amazon EC2 offers Elastic Load Balancing to spread incoming traffic over several running EC2 instances, while it checks the health of the instances registered with it. Application Load Balancers work at the application layer. In this lab you create a load balancer and a target group, create a launch template, create an Auto Scaling group attached to the load balancer, and then test the load balancer and watch it replace a failed instance.

## Lab Objectives

After this lab, you can:

1. Explain what a load balancer, a target group and a health check do.
2. Create security groups for a load balancer and for the instances behind it.
3. Create an Application Load Balancer with a listener and a target group.
4. Create a launch template and an Auto Scaling group attached to the load balancer.
5. Test load balancing and observe how a failed instance is detected and replaced.

The infrastructure you build in this lab:

![High-level architecture of Lab 2](figures/fig01.png)

## Screenshots in this lab

| File | Task | What it shows |
|---|---|---|
| `01-sg-load-balancer.png` | 1 | `LoadBalancerSecurityGroup` inbound rule: HTTP (80) from Anywhere-IPv4 |
| `02-sg-launch-template.png` | 1 | `LaunchTemplateSecurityGroup` inbound rules: HTTP (80) and SSH (22) from Anywhere-IPv4 |
| `03-target-group.png` | 2 | `LoadBalancerTargetGroup` details: name, protocol HTTP, port 80 |
| `04-health-checks.png` | 2 | The target group's **Health checks**: path `/`, interval 30 seconds, ... |
| `05-load-balancer-list.png` | 3 | **Load Balancers** page with `MyLoadBalancer` *Active* |
| `06-load-balancer-details.png` | 3 | `MyLoadBalancer` details: scheme *Internet-facing*, security group `LoadBalancerSecurityGroup` |
| `07-launch-template.png` | 4 | `AutoScalingLaunchTemplate`: Amazon Linux 2023, `t2.micro`, `LaunchTemplateSecurityGroup`, user data |
| `08-asg-list.png` | 4 | **Auto Scaling Groups** page with `MyAutoScalingGroup` |
| `09-asg-details.png` | 4 | Desired 2, minimum 2, maximum 3, target group `LoadBalancerTargetGroup` |
| `10-browser-1.png` | 5 | The load balancer's DNS name in the browser: *Hello World from (hostname)* |
| `11-browser-2.png` | 5 | The same address after refreshing, showing a **different** host name |
| `12-stop-httpd.png` | 5 | Instance Connect terminal after `sudo systemctl stop httpd.service` |
| `13-target-unhealthy.png` | 5 | Registered targets with one instance *Unhealthy* or *Draining* |
| `14-target-replaced.png` | 5 | Registered targets with a new instance *Healthy* |

Every console screenshot must show your Learner Lab user name at the top-right.

## Getting Started

### What is a load balancer?

Elastic Load Balancing spreads incoming traffic over several EC2 instances in one or more Availability Zones. It checks the health of the registered instances and sends traffic only to instances that pass the health checks. A **load balancer** is the single point of contact for clients: when it receives a request, it evaluates its listener rules, chooses a registered instance, and forwards the request.

AWS offers several types of load balancers. An **Application Load Balancer** works at the application layer (layer 7 of the OSI model); a **Network Load Balancer** works at the network layer (layer 4).

In this lab you configure an Auto Scaling group (ASG) to work with an Application Load Balancer, then test it and monitor the instances.

### Lab guidelines

- Work in **`us-east-1`**. Click the Region menu at the top-right next to your user name and select **US East (N. Virginia)**.
- Use the **resource names** given in the lab. Other names may not be allowed.
- Your permissions are limited. Some console pages may show *insufficient privileges* messages; you can ignore them.

## Task 1 — Create Security Groups

A security group is a set of firewall rules for inbound and outbound traffic. You create two: one for the load balancer, and one for the instances that the Auto Scaling group launches from the launch template.

![Infrastructure after Task 1](figures/fig02.png)

### Load balancer security group

1. Open **EC2**. In the sidebar, click **Security Groups** under **Network & Security**, then **Create security group**.
2. Name: `LoadBalancerSecurityGroup`. Description: `Allows HTTP access`. VPC: the **default VPC**.
3. Under **Inbound rules**, click **Add rule**:
   - Type: **HTTP** (port 80 is set automatically)
   - Source: **Anywhere-IPv4** (`0.0.0.0/0`)
4. Click **Create security group**.

The load balancer has one rule: HTTP, to receive web requests and talk to the instances.

> 📸 **Screenshot `01-sg-load-balancer.png`:** the inbound rules of `LoadBalancerSecurityGroup`.

### Launch template security group

1. Click **Create security group** again.
2. Name: `LaunchTemplateSecurityGroup`. Description: `Allows HTTP and SSH access`. VPC: the **default VPC**.
3. Add two inbound rules:
   - **HTTP** (port 80), source **Anywhere-IPv4**
   - **SSH** (port 22), source **Anywhere-IPv4**
4. Click **Create security group**.

The instances accept SSH, so you can connect to them, and HTTP, to serve the application behind the load balancer.

> 📸 **Screenshot `02-sg-launch-template.png`:** the inbound rules of `LaunchTemplateSecurityGroup`.

## Task 2 — Create a Target Group

A load balancer sends requests to instances called **targets**. The targets form a logical group, the **target group**. The target group also runs **health checks** on its targets and takes unhealthy ones out of service. When the target group is attached to an Auto Scaling group, the ASG replaces unhealthy instances with new ones.

![Infrastructure after Task 2](figures/fig03.png)

### Target group details

1. In the sidebar, click **Target Groups** under **Load Balancing**, then **Create target group**.
2. Target type: **Instances**. Traffic is forwarded to EC2 instances in the VPC you choose, here the default VPC of `us-east-1`.
3. Name: `LoadBalancerTargetGroup`.
4. Protocol: **HTTP**, port **80**. This is how the load balancer sends traffic to the targets.
5. VPC: the **default VPC**. All instances are launched in this VPC.

### Health checks

Keep the default health check settings, but read what they mean:

- **Health check protocol:** HTTP by default.
- **Health check path:** the path that is requested; `/` means the root of the target.
- **Advanced health check settings** set thresholds and timeouts: how many failed checks make an instance unhealthy, the time between checks, and more.

With the defaults, the root of each instance is requested every **30 seconds**; any answer other than **200** is a failed check; after **two** failed checks in a row, the instance is marked **unhealthy**.

Click **Next**.

### Register targets

You have no instances yet, so do not register any. Click **Create target group**.

> 📸 **Screenshots:** `03-target-group.png` (the target group details: name, HTTP, port 80) and `04-health-checks.png` (its **Health checks** tab).

## Task 3 — Create an Application Load Balancer

When a client reaches the load balancer, it reads the request and forwards it to a target in the target group.

![Infrastructure after Task 3](figures/fig04.png)

1. In the sidebar, click **Load Balancers** under **Load Balancing**, then **Create load balancer**.
2. Under **Application Load Balancer**, click **Create**.
3. Name: `MyLoadBalancer`.
4. Scheme: **Internet-facing**, so clients on the internet can reach it (not *Internal*).
5. IP address type: **IPv4**.
6. VPC: the **default VPC**, the same VPC as the instances.
7. **Mappings:** select **all** Availability Zones. Each mapping is a subnet in a different zone; the load balancer routes traffic to targets in the selected zones.
8. **Security groups:** remove the default security group and select `LoadBalancerSecurityGroup`.
9. **Listeners and routing:** protocol **HTTP**, port **80**. Default action: forward to `LoadBalancerTargetGroup`.
10. Click **Create load balancer**, then **View load balancer**.

> 📸 **Screenshots:** `05-load-balancer-list.png` (the list with `MyLoadBalancer` *Active*; this can take a few minutes) and `06-load-balancer-details.png` (its scheme and security group).

## Task 4 — Create an Auto Scaling Group

You create a launch template, then an Auto Scaling group that uses it and is attached to the load balancer.

![Infrastructure after Task 4](figures/fig05.png)

### Create a launch template

1. In the sidebar, click **Launch Templates** under **Instances**, then **Create launch template**.
2. Name: `AutoScalingLaunchTemplate`.
3. **Application and OS Images:** select **Amazon Linux**, then **Amazon Linux 2023**.
4. Instance type: **t2.micro**.
5. **Network settings → Firewall:** **Select existing security group**, then `LaunchTemplateSecurityGroup`.
6. Expand **Advanced details** and paste this script in **User data**:

   ```bash
   #!/bin/bash
   # Enabling admin rights
   sudo su
   # Updating system and installing httpd
   yum update -y
   yum install -y httpd.x86_64
   # Launching a simple httpd server
   systemctl start httpd.service
   systemctl enable httpd.service
   # Writing HTML file to serve on the httpd server
   echo "Hello World from ($(hostname))" > /var/www/html/index.html
   ```

7. Click **Create launch template**.

> 📸 **Screenshot `07-launch-template.png`:** the launch template's details showing the AMI, the instance type, the security group, and the user data (**Advanced details** tab).

### Create the Auto Scaling group

1. In the sidebar, click **Auto Scaling Groups** under **Auto Scaling**, then **Create Auto Scaling group**.
2. Name: `MyAutoScalingGroup`. Launch template: `AutoScalingLaunchTemplate`. Click **Next**.
3. **Network:** the default VPC. **Availability Zones and subnets:** select every zone. Click **Next**.
4. **Load balancing:** **Attach to an existing load balancer**, then choose `LoadBalancerTargetGroup`.
5. **Health checks:** turn on **Elastic Load Balancing health checks**. Click **Next**.
6. **Group size:**
   - Desired capacity: **2**
   - Minimum capacity: **2**
   - Maximum capacity: **3**
7. Click **Skip to review**, then **Create Auto Scaling group**.

> 📸 **Screenshots:** `08-asg-list.png` (the Auto Scaling Groups page with `MyAutoScalingGroup`) and `09-asg-details.png` (its capacities and the target group).

## Task 5 — Putting It All Together

You now test the load balancer and look at the health monitoring of the target group. You create nothing new.

![Infrastructure after Task 5](figures/fig06.png)

### Target group monitoring

The Auto Scaling group has launched two instances. They are registered as targets automatically.

1. Click **Target Groups** and open `LoadBalancerTargetGroup`.
2. **Registered targets** lists the instances. **Health status** shows each instance's condition: *initial*, *healthy*, *unhealthy*, *unused*, *draining* or *unavailable*. While an instance is being registered it is *initial*; it becomes *healthy* when it passes its first health checks.
3. The **Monitoring** tab plots metrics over time, such as the number of healthy and unhealthy targets and the number of requests.

> **Note:** Health status and monitoring data can take several minutes to appear after the instances launch.

### Access the load balancer

1. Wait until both targets are **healthy**.
2. Click **Load Balancers** and select `MyLoadBalancer`.
3. Copy its **DNS name** from the **Details** section.
4. Open it in a new browser tab (with `http://`).

You see *Hello World from (...)* with the host name of the instance that served your request. Refresh the page several times: the host name changes as the load balancer sends your requests to different instances.

> 📸 **Screenshots:** `10-browser-1.png` and `11-browser-2.png`, the same address showing two different host names.

### Simulate an application failure

An Application Load Balancer checks the **application**, not only the instance. If the application on an instance fails its health checks, the instance is replaced by a new one. You simulate this by stopping the web server on one instance.

1. Click **Instances**, select one of the running instances, and click **Connect**.
2. Click **Connect** to open EC2 Instance Connect.
3. Stop the web server:

   ```bash
   sudo systemctl stop httpd.service
   ```

   > 📸 **Screenshot `12-stop-httpd.png`:** the terminal after this command.

The instance is still running, but its application no longer answers, so it fails the health checks.

Go back to `LoadBalancerTargetGroup` → **Targets**. After a few minutes (two failed checks), the instance becomes **unhealthy**, then **draining** while it is deregistered and taken out of service. The Auto Scaling group launches a new instance, which becomes **healthy** once it passes its health checks.

> 📸 **Screenshots:** `13-target-unhealthy.png` (one target *Unhealthy* or *Draining*) and `14-target-replaced.png` (the new target *Healthy*). Refresh the page to follow the change.

## Task 6 — Clean Up

Take all screenshots **before** you clean up. Delete in the reverse order of creation.

**Delete the Auto Scaling group**

1. Click **Auto Scaling Groups** and select `MyAutoScalingGroup`.
2. Click **Actions → Delete**, type `delete`, and click **Delete**.

> **Note:** Deleting the ASG terminates all its instances. This can take up to ten minutes.

**Delete the launch template**

1. Click **Launch Templates** and select `AutoScalingLaunchTemplate`.
2. Click **Actions → Delete template**, type `Delete`, and click **Delete**.

**Delete the load balancer**

1. Click **Load Balancers** and select `MyLoadBalancer`.
2. Click **Actions → Delete load balancer**, type `confirm`, and click **Delete**.

**Delete the target group**

1. Click **Target Groups** and select `LoadBalancerTargetGroup`.
2. Click **Actions → Delete**, then **Yes, delete**.

**Delete the security groups**

1. When the instances are terminated, click **Security Groups**.
2. Select `LoadBalancerSecurityGroup` and `LaunchTemplateSecurityGroup`.
3. Click **Actions → Delete security groups**, then **Delete**.

# Submission

1. Make the lab folder and copy your 14 screenshots into `images/`:

   ```bash
   mkdir -p ~/cc-gic-YOUR_ID/cc-lab-YOUR_ID/lab2/images
   ```

2. Copy the [report template](README.md) to `cc-lab-YOUR_ID/lab2/README.md` and fill it in.
3. Check the structure:

   ```text
   cc-lab-YOUR_ID/
   └── lab2/
       ├── README.md
       └── images/
           ├── 01-sg-load-balancer.png
           ├── 02-sg-launch-template.png
           ├── 03-target-group.png
           ├── 04-health-checks.png
           ├── 05-load-balancer-list.png
           ├── 06-load-balancer-details.png
           ├── 07-launch-template.png
           ├── 08-asg-list.png
           ├── 09-asg-details.png
           ├── 10-browser-1.png
           ├── 11-browser-2.png
           ├── 12-stop-httpd.png
           ├── 13-target-unhealthy.png
           └── 14-target-replaced.png
   ```

4. Commit and push:

   ```bash
   cd ~/cc-gic-YOUR_ID
   git add .
   git commit -m "Lab 2: load balancer and Auto Scaling group"
   git push
   ```
