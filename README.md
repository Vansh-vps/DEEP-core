# 🟢 GitHub Heartbeat & Automated Commit Maker

An automated tool to **backfill past GitHub contribution activity ("old heartbeats")** and maintain **automated daily commits 24/7 in the cloud**—even when you are offline or your PC is turned off.

---

## 🚀 Features

- **Backfill Old Heartbeats**: Populate your past GitHub contribution graph with realistic or solid green squares for any time frame (past 3 months, 6 months, 1 year, or custom date ranges).
- **24/7 Automated Daily Commits**: Uses free GitHub Actions cloud cron runners—commits automatically even when your computer is off or you have no internet.
- **Two Commit Styles**:
  - `natural` (Recommended): 85–90% active days, 1–4 commits per day, subtle weekend variations. Mimics real development activity.
  - `solid`: 100% active days, guaranteed commits every single day.
- **Interactive CLI & Windows One-Click**: Double click `run.bat` or run `python commit_maker.py`.
- **Pure Standard Python**: Zero external dependencies required.

---

## ⚙️ Quick Start Setup (3 Steps)

### Step 1: Create a Repository on GitHub
1. Go to [github.com/new](https://github.com/new) and create a repository (e.g. `github-heartbeat` or any name).
2. You can make it **Public** or **Private** (see Private Repos note below).
3. Do **not** initialize it with README, .gitignore, or license (we already have them here).

### Step 2: Link Your Local Folder to GitHub
Open your terminal in this directory (`f:\commit maker`) and run:

```bash
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git
git branch -M main
```

*(Replace `<YOUR_GITHUB_USERNAME>` and `<YOUR_REPO_NAME>` with your actual GitHub details)*

### Step 3: Enable GitHub Actions Workflow Permissions
To let GitHub Actions commit daily in the cloud without needing personal tokens:
1. Open your repository on GitHub.
2. Go to **Settings** > **Actions** > **General**.
3. Scroll down to **Workflow permissions**.
4. Select **"Read and write permissions"** and click **Save**.

---

## 🕒 How to Make / Backfill Old Heartbeats

You can backfill your past contribution history in two ways:

### Option A: Interactive Menu (Easiest)
Just double-click **`run.bat`** (or run `python commit_maker.py` in terminal).
Follow the prompts to choose your date range and pattern style.

### Option B: Command Line

**Past 1 Year (365 days) - Natural human-like pattern:**
```bash
python commit_maker.py backfill --days 365 --style natural
```

**Past 1 Year - Solid green (every single day):**
```bash
python commit_maker.py backfill --days 365 --style solid
```

**Past 6 Months (180 days):**
```bash
python commit_maker.py backfill --days 180 --style natural
```

**Custom Date Range:**
```bash
python commit_maker.py backfill --start 2025-01-01 --end 2025-12-31 --style natural
```

### Push to GitHub:
Once you generate the backfilled commits, push them to GitHub:
```bash
git push -u origin main
```
Your GitHub contribution graph will update immediately!

---

## ⚡ Daily Commits (When Offline)

The repository includes a GitHub Actions workflow located at:
[`.github/workflows/daily-heartbeat.yml`](.github/workflows/daily-heartbeat.yml)

- It runs **twice a day** automatically on GitHub's cloud servers.
- It commits a heartbeat timestamp to `heartbeat.txt` and pushes to `main`.
- **You do NOT need your computer on or internet connected.** GitHub executes the workflow on their servers for free.
- **Manual Trigger**: You can also go to the **Actions** tab on your GitHub repository, click **Daily Heartbeat Committer**, and click **Run workflow** to test it anytime.

---

## ⚠️ Important GitHub Profile Settings

For contributions to show on your GitHub profile:

1. **Email Match**: Commits must use the email associated with your GitHub account:
   - Currently configured for: `vanshpratap2323@gmail.com`
   - If your GitHub account uses a different email, update it in `commit_maker.py` and `.github/workflows/daily-heartbeat.yml`.
2. **Private Repository Visibility**:
   - If you set your repository to **Private**, GitHub hides private contributions by default.
   - To make private contributions visible on your profile:
     - Go to your GitHub profile page (`https://github.com/<your-username>`)
     - Above your contribution graph, click **Contribution settings** (dropdown on the right)
     - Check **"Private contributions"**
3. **Default Branch**:
   - Commits only count toward the contribution graph if they are on the repository's default branch (`main`).

---

## 📊 Checking Your Stats

To see summary statistics of all commits currently in the repository:
```bash
python commit_maker.py stats
```

Co-author test
