from pydriller import Repository

# Input
repo_url = "https://github.com/apache/lucene"
issue_ids = ["LUCENE-12", "LUCENE-17", "LUCENE-701", "LUCENE-1200", "LUCENE-1799"]

# Storage
unique_commits = set()
commit_file_map = {}   # commit -> set(files)
dmm_scores = []        # (unit_size + complexity + interfacing)

# Traverse repo
for commit in Repository(repo_url).traverse_commits():
    message = commit.msg.upper()

    # Check if commit references any issue ID
    if any(issue in message for issue in issue_ids):
        unique_commits.add(commit.hash)

        # Track unique files per commit
        files = set()
        for mod in commit.modified_files:
            if mod.new_path:
                files.add(mod.new_path)
            elif mod.old_path:
                files.add(mod.old_path)

        commit_file_map[commit.hash] = files

        # DMM metrics (may be None sometimes)
        if (commit.dmm_unit_size is not None and
            commit.dmm_unit_complexity is not None and
            commit.dmm_unit_interfacing is not None):

            total_dmm = (commit.dmm_unit_size +
                         commit.dmm_unit_complexity +
                         commit.dmm_unit_interfacing)

            dmm_scores.append(total_dmm)

# --- Calculations ---
total_commits = len(unique_commits)

# Total unique files across all commits
all_unique_files = set()
for files in commit_file_map.values():
    all_unique_files.update(files)

avg_unique_files = len(all_unique_files) / total_commits if total_commits > 0 else 0
avg_dmm = sum(dmm_scores) / total_commits if total_commits > 0 else 0

# --- Output ---
print("Total Commits:", total_commits)
print("Avg Unique Files Changed:", avg_unique_files)
print("Average DMM Score:", avg_dmm)