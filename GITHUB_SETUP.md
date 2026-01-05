# GitHub Repository Setup Instructions

## ✅ Files Created

The following files have been set up for your GitHub repository:

```
New-ONA/
├── .gitignore                          # Ignores Python, Node, Docker, secrets
├── .env.example                        # Environment variables template
├── LICENSE                             # MIT License
├── CHANGELOG.md                        # Version history tracking
├── CONTRIBUTING.md                     # Contribution guidelines
└── .github/
    ├── FUNDING.yml                     # Sponsor configuration
    ├── pull_request_template.md        # PR template
    └── ISSUE_TEMPLATE/
        ├── bug_report.md               # Bug report template
        └── feature_request.md          # Feature request template
```

---

## 🚀 Step-by-Step Setup

### 1. Initialize Git Repository Locally

Open PowerShell in the `New-ONA` directory and run:

```powershell
# Make sure you're in the right directory
cd G:\ONA-Development\New-ONA

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: ONA Platform v2.0 planning and architecture"
```

### 2. Create Repository on GitHub

**Option A: Via GitHub Website**

1. Go to https://github.com/new
2. Repository name: `ONA-Platform` (or your preferred name)
3. Description: `Organizational Network Analysis Platform v2.0 - React + FastAPI with Neo4j`
4. Choose: **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

**Option B: Via GitHub CLI** (if installed)

```powershell
# Install GitHub CLI first if needed: winget install GitHub.cli

gh repo create ONA-Platform --public --source=. --remote=origin
```

### 3. Link Local Repository to GitHub

After creating the repo on GitHub, you'll see instructions. Run these commands:

```powershell
# Add remote repository (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/ONA-Platform.git

# Verify remote was added
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🔧 Configure Repository Settings (on GitHub)

After pushing, configure your repository on GitHub:

### 1. Repository Settings

Go to: `Settings` → `General`

**Features to enable:**

- ✅ Issues
- ✅ Projects (for project management)
- ✅ Wiki (optional)
- ✅ Discussions (for community Q&A)

### 2. Branch Protection

Go to: `Settings` → `Branches` → `Add rule`

**For `main` branch:**

- ✅ Require a pull request before merging
- ✅ Require approvals (1-2 reviewers)
- ✅ Require status checks to pass
- ✅ Require conversation resolution before merging
- ✅ Include administrators (optional)

### 3. Add Topics/Tags

Go to repository main page → Click ⚙️ (gear icon) next to "About"

**Suggested topics:**

- `organizational-network-analysis`
- `react`
- `fastapi`
- `neo4j`
- `typescript`
- `python`
- `graph-database`
- `network-visualization`
- `social-network-analysis`

**Add description:**

```
Organizational Network Analysis Platform v2.0 - Modern React + FastAPI application with Neo4j graph database, multi-source data ingestion, and horizontal scalability
```

**Add website:** (when deployed)

### 4. Create Labels

Go to: `Issues` → `Labels`

**Suggested labels:**

- `phase-1`, `phase-2`, ... `phase-10` (for development phases)
- `backend`, `frontend`, `database`, `infrastructure`
- `license-demo`, `license-basic`, `license-pro`, `license-enterprise`
- `performance`, `security`, `scalability`
- `good-first-issue`, `help-wanted`

---

## 📋 After Setup Checklist

- [ ] Repository created on GitHub
- [ ] Local repo pushed to GitHub
- [ ] Branch protection enabled on `main`
- [ ] Topics/tags added
- [ ] Description added
- [ ] README.md displays correctly
- [ ] License visible in repository
- [ ] Issues enabled
- [ ] `.gitignore` working (no unwanted files tracked)

---

## 👥 Collaborator Setup (if team project)

Go to: `Settings` → `Collaborators and teams`

1. Add collaborators by username
2. Set permissions (Read, Write, Admin)
3. Send invitations

---

## 🔒 Security Setup

### 1. Enable Security Features

Go to: `Settings` → `Security & analysis`

Enable:

- ✅ Dependency graph
- ✅ Dependabot alerts
- ✅ Dependabot security updates
- ✅ Secret scanning (if available)

### 2. Add .env to .gitignore (already done)

Verify `.env` is in `.gitignore`:

```bash
# Check if .env is ignored
git check-ignore -v .env
```

### 3. Never Commit Secrets

**Before committing, always check:**

```powershell
# View what will be committed
git status

# View diff
git diff

# Search for potential secrets (PowerShell)
Select-String -Pattern "password|secret|key|token" -Path * -Exclude .gitignore,.env.example
```

---

## 📦 Optional: GitHub Actions Setup (CI/CD)

Create `.github/workflows/` directory for automated testing (can be done later in Phase 1).

Example workflows to add later:

- `backend-tests.yml` - Python tests
- `frontend-tests.yml` - React tests
- `security-scan.yml` - Dependency scanning
- `deploy.yml` - Deployment automation

---

## 🎯 Next Steps After GitHub Setup

1. **Share repository link** with team/stakeholders
2. **Create first issue**: "Phase 1: Foundation & Setup"
3. **Create project board**: Map development plan to GitHub Projects
4. **Set up development branches**:
   ```powershell
   git checkout -b develop
   git push -u origin develop
   ```
5. **Start Phase 1 development** following DEVELOPMENT_PLAN.md

---

## 📝 Common Git Commands Reference

```powershell
# Check status
git status

# Create new branch
git checkout -b feature/your-feature

# Stage changes
git add .
git add specific-file.py

# Commit changes
git commit -m "feat(analytics): add centrality calculation"

# Push to GitHub
git push origin feature/your-feature

# Pull latest changes
git pull origin main

# View commit history
git log --oneline

# Discard local changes
git checkout -- filename

# Update from main
git checkout main
git pull
git checkout feature/your-feature
git merge main
```

---

## 🆘 Troubleshooting

### "Authentication failed"

Use GitHub Personal Access Token instead of password:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` permissions
3. Use token as password when pushing

Or use SSH instead:

```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to SSH agent and GitHub
# Then change remote to SSH
git remote set-url origin git@github.com:YOUR-USERNAME/ONA-Platform.git
```

### "Remote already exists"

```powershell
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/ONA-Platform.git
```

### Large files issue

If you accidentally committed large files:

```powershell
# Remove from git but keep locally
git rm --cached large-file.db

# Add to .gitignore
echo "large-file.db" >> .gitignore

# Commit the removal
git commit -m "Remove large file from tracking"
```

---

## ✅ Verification

After setup, verify everything is working:

```powershell
# 1. Check remote is set
git remote -v

# 2. Check current branch
git branch

# 3. Check repository URL
git config --get remote.origin.url

# 4. Verify .gitignore is working
git status  # Should not show .env, __pycache__, node_modules, etc.
```

---

**Your repository is now ready! 🎉**

Visit: `https://github.com/YOUR-USERNAME/ONA-Platform`

Share the link with your team and start development!
