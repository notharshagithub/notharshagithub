# Setup & Installation Guide

This profile utilizes automated GitHub Workflows to keep metrics, the contribution snake, and the activity feed live and updated. Follow these steps to configure the necessary permissions and run the updates.

## 🛠️ Workflows Overview

1. **Profile Activity Feed (`profile-update.yml`):** Runs every 6 hours. Runs `update_readme.py` to fetch public repositories and public events, then commits changes to the `main` branch.
2. **Monochrome Contribution Snake (`snake.yml`):** Runs every 6 hours. Generates light/dark monochrome SVGs and pushes them to the `output` branch.
3. **Advanced Metrics (`metrics.yml`):** Runs every 12 hours. Uses `lowlighter/metrics` to build a repository analytics dashboard SVG and pushes it to the `output` branch.

---

## 🔑 Permissions & Token Setup

### 1. Enable Workflow Permissions
By default, GitHub Actions have read-only permissions. You need to grant them write permissions to commit changes back to the repository:
1. Go to your repository settings page: `https://github.com/notharshagithub/notharshagithub/settings`
2. In the left sidebar, navigate to **Actions** > **General**.
3. Scroll down to **Workflow permissions**.
4. Select **Read and write permissions**.
5. Click **Save**.

### 2. Configure GitHub Token for Metrics
If you run into API rate limits for `lowlighter/metrics` or wish to display private repository data in your metrics:
1. Generate a Personal Access Token (PAT) with `repo` scope from your developer settings.
2. Go to repository settings > **Secrets and variables** > **Actions**.
3. Create a repository secret named `METRICS_TOKEN` (or use the default `GITHUB_TOKEN` for public data).

---

## 🚀 Manual Run
You don't need to wait for the cron schedule to see it in action. You can trigger them immediately:
1. Go to the **Actions** tab on your GitHub repository.
2. Select any workflow in the left sidebar (e.g., `Update Profile Activity`).
3. Click the **Run workflow** dropdown on the right side.
4. Select the branch and click **Run workflow**.

---

## 🗂️ File Structure

```
.
├── .github/
│   └── workflows/
│       ├── metrics.yml           # Generates advanced metrics SVGs
│       ├── profile-update.yml    # Auto-updates README with activity events
│       └── snake.yml             # Generates contribution snake SVG
├── README.md                     # Elite Monochrome Profile Portfolio
├── SETUP.md                      # This Setup instructions file
└── update_readme.py              # Script that runs on Actions to fetch live API data
```
