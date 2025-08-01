import json

def load_mock_commits(path="data/mock_commits.json"):
    with open(path, "r") as f:
        data = json.load(f)
    return [item["message"] for item in data]

def format_commits(commits):
    categories = {
        "feat": "### Features",
        "fix": "### Bug Fixes",
        "perf": "### Performance Improvements",
        "docs": "### Documentation",
        "refactor": "### Refactoring"
    }

    grouped = {v: [] for v in categories.values()}
    for msg in commits:
        for prefix, section in categories.items():
            if msg.startswith(prefix):
                grouped[section].append(f"- {msg}")
                break

    formatted = "\n".join(
        f"{section}\n" + "\n".join(items)
        for section, items in grouped.items() if items
    )
    return formatted