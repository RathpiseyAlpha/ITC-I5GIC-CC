# Student setup: AWS Academy and GitHub

Do this once, before Lab 1. Every Cloud Lab is done in your own **AWS Academy Learner Lab** account, and every result is handed in through your own **GitHub repository**. You do not hand in Word or PDF files in this course.

## 1. AWS Academy Learner Lab

1. Open the course in AWS Academy and start the **Learner Lab**. Wait until the indicator next to "AWS" turns green, then click **AWS** to open the AWS Management Console.
2. Work in the Region the lab names, normally **US East (N. Virginia) `us-east-1`**. Other Regions are restricted.
3. Your account has a budget of **50 USD**. Running resources keep costing money after you close the browser, so do the **Clean Up** section of every lab.
4. You cannot create IAM roles in the Learner Lab. When a lab needs a role, use the ones that already exist: **`LabRole`** (for services such as Lambda, ECS and CodeBuild) and **`LabInstanceProfile`** (for EC2 instances).
5. The Learner Lab shows temporary credentials under **AWS Details → AWS CLI**. Some labs ask you to use them. They are secrets: never paste them into a file that you commit, and never show them in a screenshot.

### Screenshot rule

The top-right corner of the console shows your Learner Lab user name. **Every console screenshot must show this name.** It proves the work was done in your own account. A screenshot of a terminal or a browser page must show the command or address that produced it.

## 2. Create your GitHub repository

1. Create a GitHub account if you do not have one.
2. On GitHub, create an **empty** repository named **`CC-GIC-YOUR_ID`** (no README, no license, no `.gitignore`). Replace `YOUR_ID` with your student ID, for example `CC-GIC-e20230123`.
3. Install Git on your computer. On Windows, use **Git Bash** (comes with [Git for Windows](https://git-scm.com/download/win)) or WSL. All commands in the labs are written for Bash.
4. Tell Git who you are (first time only):

   ```bash
   git config --global user.name "YOUR NAME"
   git config --global user.email "YOUR_EMAIL"
   ```

## 3. Create your course folder and connect it to GitHub

Replace `YOUR_ID` with your student ID and `YOUR_USERNAME` with your GitHub user name.

```bash
mkdir -p ~/cc-gic-YOUR_ID/cc-lab-YOUR_ID
cd ~/cc-gic-YOUR_ID
git init
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/CC-GIC-YOUR_ID.git
```

Create a file named `.gitignore` in `~/cc-gic-YOUR_ID` with this content. It stops Git from uploading keys, credentials and large generated files:

```gitignore
# Keys and credentials: never commit these
*.pem
*.ppk
credentials
.env
.aws/

# Terraform working files (Lab 10)
.terraform/
*.tfstate
*.tfstate.*
*.zip

# Node.js (Lab 11)
node_modules/
```

Make the first commit and push:

```bash
git add .gitignore
git commit -m "Set up course repository"
git push -u origin main
```

GitHub asks for your user name and a **personal access token**, not your password. Create a token on GitHub under **Settings → Developer settings → Personal access tokens**.

## 4. Your submission repository

Every lab goes in its own folder `labN` inside `cc-lab-YOUR_ID`:

```text
cc-gic-YOUR_ID/                    # GitHub repository CC-GIC-YOUR_ID
├── .gitignore
└── cc-lab-YOUR_ID/                # Lab submissions
    ├── lab1/
    │   ├── README.md              # Your lab report (copied from the lab's template)
    │   └── images/                # Your screenshots, named as the lab lists them
    │       ├── 01-security-group.png
    │       └── ...
    ├── lab2/
    │   ├── README.md
    │   └── images/
    └── ...
```

Some labs ask for extra files next to `README.md` (for example the templates of Lab 10 or the CSV export of Lab 8). Each lab lists exactly what it expects.

## 5. Submitting a lab

Each lab ends with a **Submission** section. The steps are always the same:

1. Make the lab folder and its `images` folder:

   ```bash
   mkdir -p ~/cc-gic-YOUR_ID/cc-lab-YOUR_ID/labN/images
   ```

2. Save each screenshot in `images/` with **exactly** the file name the lab gives. Use PNG.
3. Copy the lab's report template (`README.md` in the lab's folder of the course materials) to `cc-lab-YOUR_ID/labN/README.md` and fill it in. Write the answers in your own words. In VS Code, `Ctrl+Shift+V` previews it.
4. Commit and push from the top folder:

   ```bash
   cd ~/cc-gic-YOUR_ID
   git add .
   git commit -m "Lab N: screenshots and report"
   git push
   ```

5. Open your repository on GitHub and check that the report shows every screenshot. A broken image usually means the file name in `README.md` and the file name in `images/` are different (names are case-sensitive).

You can push as often as you like. Only what is on GitHub at the deadline is marked.
