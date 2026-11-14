"""
GitHub Heartbeat & Commit Maker
================================
Automate past commit history (backfilling) and configure automated daily
cloud commits using GitHub Actions (runs even when your computer is off).
"""

import os
import sys
import random
import argparse
import subprocess
from datetime import datetime, timedelta, time

HEARTBEAT_FILE = "heartbeat.txt"

# Default Git Author / Committer info (can be overridden)
DEFAULT_NAME = "Vansh pratap"
DEFAULT_EMAIL = "vanshpratap2323@gmail.com"

COMMIT_MESSAGES = [
    "chore: daily heartbeat sync",
    "chore: system health check pulse",
    "chore: routine heartbeat record",
    "docs: update activity log",
    "chore: automated maintenance pulse",
    "perf: optimize activity log entries",
    "chore: update heartbeat timestamp",
    "chore: keep-alive heartbeat ping",
    "ci: scheduled health sync",
    "chore: activity heartbeat check",
]


def run_git(args, env_override=None, capture=True):
    """Run a git command safely and return output."""
    env = os.environ.copy()
    if env_override:
        env.update(env_override)
    try:
        res = subprocess.run(
            ["git"] + args,
            capture_output=capture,
            text=True,
            check=True,
            env=env
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        err = e.stderr.strip() if e.stderr else str(e)
        raise RuntimeError(f"Git command failed: git {' '.join(args)}\nError: {err}")


def get_git_user():
    """Retrieve current git user or fallback to defaults."""
    try:
        name = run_git(["config", "user.name"]) or DEFAULT_NAME
    except Exception:
        name = DEFAULT_NAME
    try:
        email = run_git(["config", "user.email"]) or DEFAULT_EMAIL
    except Exception:
        email = DEFAULT_EMAIL
    return name, email


def create_commit_at(target_datetime, message=None, author_name=None, author_email=None):
    """
    Creates a commit at a specific past or present datetime.
    Both GIT_AUTHOR_DATE and GIT_COMMITTER_DATE are set to ensure
    GitHub's contribution graph registers the commit properly.
    """
    name, email = get_git_user()
    name = author_name or name
    email = author_email or email

    date_str = target_datetime.strftime("%Y-%m-%d %H:%M:%S")
    iso_date = target_datetime.isoformat()

    if not message:
        message = random.choice(COMMIT_MESSAGES)

    # Append entry to heartbeat log
    with open(HEARTBEAT_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{date_str}] Heartbeat pulse | {message}\n")

    env = {
        "GIT_AUTHOR_NAME": name,
        "GIT_AUTHOR_EMAIL": email,
        "GIT_AUTHOR_DATE": iso_date,
        "GIT_COMMITTER_NAME": name,
        "GIT_COMMITTER_EMAIL": email,
        "GIT_COMMITTER_DATE": iso_date,
    }

    run_git(["add", HEARTBEAT_FILE])
    run_git(["commit", "-m", f"{message} [{date_str}]", "--date", iso_date], env_override=env)


def backfill_history(start_date, end_date, style="natural", min_commits=1, max_commits=4, probability=0.88):
    """
    Generate commit history across a date range.
    - style='solid': Commits every single day without skips.
    - style='natural': Randomized activity mimicking realistic human activity.
    """
    if start_date > end_date:
        raise ValueError("Start date must be before or equal to end date.")

    current = start_date
    total_days = (end_date - start_date).days + 1
    total_commits = 0
    days_with_commits = 0

    print(f"\n=======================================================")
    print(f" Starting Commit Backfill")
    print(f" Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} ({total_days} days)")
    print(f" Mode : {style.upper()} (min: {min_commits}, max: {max_commits})")
    print(f"=======================================================\n")

    while current <= end_date:
        is_weekend = current.weekday() in (5, 6)
        
        if style == "solid":
            should_commit = True
        else:
            # Natural mode: slightly lower probability on weekends
            effective_prob = probability * 0.75 if is_weekend else probability
            should_commit = random.random() < effective_prob

        if should_commit:
            num_commits = random.randint(min_commits, max_commits)
            days_with_commits += 1

            for _ in range(num_commits):
                # Pick realistic random hours between 09:00 and 22:30
                hour = random.randint(9, 22)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                commit_dt = datetime.combine(current, time(hour, minute, second))

                create_commit_at(commit_dt)
                total_commits += 1

        # Advance one day
        current += timedelta(days=1)

    print(f"\nBackfill Complete!")
    print(f" - Days covered: {total_days}")
    print(f" - Active days: {days_with_commits}")
    print(f" - Total commits created: {total_commits}")
    print(f"\nTip: Run 'git log --oneline -n 10' or 'python commit_maker.py stats' to verify.")


def single_daily_commit(count=1):
    """Create heartbeat commit(s) for the current moment."""
    now = datetime.now()
    for i in range(count):
        create_commit_at(now)
        print(f"Created daily heartbeat commit #{i+1} at {now.strftime('%Y-%m-%d %H:%M:%S')}")


def get_stats():
    """Print statistics about existing commits in the repo."""
    try:
        count_str = run_git(["rev-list", "--count", "HEAD"])
        commit_count = int(count_str)
    except Exception:
        print("No commits yet in this repository.")
        return

    first_commit_date = run_git(["log", "--reverse", "--format=%ad", "--date=short", "-n", "1"])
    latest_commit_date = run_git(["log", "--format=%ad", "--date=short", "-n", "1"])
    author_name, author_email = get_git_user()

    print("\n=== Repository Commit Statistics ===")
    print(f" Total Commits  : {commit_count}")
    print(f" First Commit   : {first_commit_date}")
    print(f" Latest Commit  : {latest_commit_date}")
    print(f" Configured User: {author_name} <{author_email}>")
    print("====================================\n")


def interactive_wizard():
    """Interactive CLI menu for beginners."""
    print("======================================================")
    print("    GitHub Heartbeat & Activity Commit Generator     ")
    print("======================================================")
    name, email = get_git_user()
    print(f"Detected Git User: {name} <{email}>\n")
    print("What would you like to do?")
    print("  1) Backfill past commits (e.g. past 1 year, 6 months, or custom)")
    print("  2) Make a daily heartbeat commit for today")
    print("  3) View commit statistics")
    print("  4) Exit")
    
    choice = input("\nEnter choice [1-4]: ").strip()

    if choice == "1":
        print("\n--- Backfill Configuration ---")
        print("Quick Presets:")
        print("  1. Past 1 Year (365 days)")
        print("  2. Past 6 Months (180 days)")
        print("  3. Past 3 Months (90 days)")
        print("  4. Custom Date Range (YYYY-MM-DD)")

        preset = input("Choose preset [1-4, default=1]: ").strip() or "1"
        today = datetime.now().date()

        if preset == "1":
            start_date = today - timedelta(days=365)
            end_date = today - timedelta(days=1)
        elif preset == "2":
            start_date = today - timedelta(days=180)
            end_date = today - timedelta(days=1)
        elif preset == "3":
            start_date = today - timedelta(days=90)
            end_date = today - timedelta(days=1)
        elif preset == "4":
            s_str = input("Enter start date (YYYY-MM-DD): ").strip()
            e_str = input("Enter end date   (YYYY-MM-DD) [default=yesterday]: ").strip()
            start_date = datetime.strptime(s_str, "%Y-%m-%d").date()
            if e_str:
                end_date = datetime.strptime(e_str, "%Y-%m-%d").date()
            else:
                end_date = today - timedelta(days=1)
        else:
            print("Invalid choice, defaulting to past 365 days.")
            start_date = today - timedelta(days=365)
            end_date = today - timedelta(days=1)

        print("\nCommit Density Style:")
        print("  1. Natural (Recommended - 88% active days, 1-4 commits/day, looks organic)")
        print("  2. Solid Green (100% active days, guaranteed commits every day)")
        style_choice = input("Choose style [1 or 2, default=1]: ").strip() or "1"
        style = "solid" if style_choice == "2" else "natural"

        backfill_history(start_date, end_date, style=style)

    elif choice == "2":
        count_input = input("How many commits for today? [default=1]: ").strip() or "1"
        single_daily_commit(int(count_input))
    elif choice == "3":
        get_stats()
    else:
        print("Exiting.")


def main():
    parser = argparse.ArgumentParser(description="GitHub Heartbeat & Activity Committer")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: backfill
    backfill_parser = subparsers.add_parser("backfill", help="Backfill past commits")
    backfill_parser.add_argument("--days", type=int, help="Number of past days from today")
    backfill_parser.add_argument("--start", type=str, help="Start date (YYYY-MM-DD)")
    backfill_parser.add_argument("--end", type=str, help="End date (YYYY-MM-DD)")
    backfill_parser.add_argument("--style", choices=["natural", "solid"], default="natural", help="Pattern style")
    backfill_parser.add_argument("--min-commits", type=int, default=1, help="Minimum commits per active day")
    backfill_parser.add_argument("--max-commits", type=int, default=4, help="Maximum commits per active day")
    backfill_parser.add_argument("--frequency", type=float, default=0.88, help="Probability of commit on weekday (0.0 to 1.0)")

    # Subcommand: daily
    daily_parser = subparsers.add_parser("daily", help="Make a commit for current day/time")
    daily_parser.add_argument("--count", type=int, default=1, help="Number of commits to make")

    # Subcommand: stats
    subparsers.add_parser("stats", help="Display commit statistics")

    args = parser.parse_args()

    if not args.command:
        interactive_wizard()
        return

    if args.command == "backfill":
        today = datetime.now().date()
        if args.days:
            start_date = today - timedelta(days=args.days)
            end_date = today - timedelta(days=1)
        elif args.start:
            start_date = datetime.strptime(args.start, "%Y-%m-%d").date()
            end_date = datetime.strptime(args.end, "%Y-%m-%d").date() if args.end else (today - timedelta(days=1))
        else:
            # Default to 365 days
            start_date = today - timedelta(days=365)
            end_date = today - timedelta(days=1)

        backfill_history(
            start_date,
            end_date,
            style=args.style,
            min_commits=args.min_commits,
            max_commits=args.max_commits,
            probability=args.frequency
        )

    elif args.command == "daily":
        single_daily_commit(args.count)

    elif args.command == "stats":
        get_stats()


if __name__ == "__main__":
    main()
