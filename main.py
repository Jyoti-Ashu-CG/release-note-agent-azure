# main.py
import os
from datetime import datetime
from github import Github
from release_note_agent.generator import ReleaseNoteGenerator
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_loaded = load_dotenv()
if not dotenv_loaded:
    print("⚠️  Warning: .env file not found. Make sure environment variables are set.")

token = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
repo_name = "Jyoti-Ashu-CG/release-note-agent"  # 🔁 Replace with actual owner/repo

if not token:
    raise ValueError("❌ GITHUB_TOKEN not found in environment. Please set it in a .env file or your system environment variables.")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in environment. Please set it in a .env file or your system environment variables.")

# Connect to GitHub
g = Github(token)
try:
    repo = g.get_repo(repo_name)
except Exception as e:
    raise RuntimeError(f"❌ Failed to access repo '{repo_name}': {e}")

# Detect latest tag
try:
    tags = repo.get_tags()
    version = tags[0].name if tags.totalCount > 0 else "v0.1.0"
except Exception as e:
    print(f"⚠️ Could not fetch tags: {e}")
    version = "v0.1.0"

# Fetch recent closed PRs
pulls = repo.get_pulls(state='closed', sort='updated', direction='desc')
pulls_list = list(pulls)

if not pulls_list:
    print("⚠️ No closed pull requests found. Skipping release note generation.")
    exit(0)

# Collect commit messages and PR descriptions
messages = []
for pr in pulls_list[:5]:  # Last 5 PRs
    pr_title = pr.title or "No title"
    pr_body = pr.body or "No description"
    messages.append(f"PR: {pr_title}\n{pr_body}")
    try:
        for commit in pr.get_commits():
            messages.append(f"- {commit.commit.message}")
    except Exception as e:
        print(f"⚠️ Could not fetch commits for PR #{pr.number}: {e}")

# Combine messages
commit_text = "\n".join(messages)

# Generate release notes
generator = ReleaseNoteGenerator()
raw_notes = generator.generate(commit_text).content.strip()

# Remove duplicate header if present
cleaned_notes = raw_notes.replace("# Release Notes", "").strip()

# Remove empty sections
sections = ["✨ Features", "🐛 Bug Fixes", "🛠️ Improvements", "📚 Documentation"]
lines = cleaned_notes.splitlines()
filtered_lines = []
skip_next = False

for i, line in enumerate(lines):
    if any(line.strip().startswith(f"### {s}") for s in sections):
        # Check if next line is empty or a placeholder
        next_line = lines[i + 1] if i + 1 < len(lines) else ""
        if not next_line.strip() or "no changes" in next_line.lower():
            skip_next = True
            continue
    if skip_next:
        skip_next = False
        continue
    filtered_lines.append(line)

final_body = "\n".join(filtered_lines).strip()

# If no user-facing sections remain, add internal-only message
if not any(s in final_body for s in sections):
    final_body += "\n\n(No user-visible features or changes in this release.)"

# Add version and date header
release_date = datetime.now().strftime("%Y-%m-%d")
header = f"# 📝 Release Notes\n\n## {version}\n📅 Released on: {release_date}\n\n"

full_notes = header + final_body + "\n"

# Save to file
with open("RELEASE_NOTES.md", "w", encoding="utf-8") as f:
    f.write(full_notes)

print(f"✅ RELEASE_NOTES.md generated for {version} on {release_date}.")