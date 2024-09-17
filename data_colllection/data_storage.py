
from github import Github
from repo_details import save_commits_to_csv, save_pull_requests_to_csv, save_issues_to_csv, save_reviews_to_csv

g = Github("")



repo = g.get_repo("opencv/opencv")

commits_csv = "commits.csv"
pull_requests_csv = "pull_requests.csv"
issues_csv = "issues.csv"
reviews_csv = "reviews.csv"

# Call the functions to save each type of data into separate CSV files
save_commits_to_csv(repo, commits_csv)
print(f"Commits saved to {commits_csv}")

save_pull_requests_to_csv(repo, pull_requests_csv)
print(f"Pull requests saved to {pull_requests_csv}")

save_issues_to_csv(repo, issues_csv)
print(f"Issues saved to {issues_csv}")

save_reviews_to_csv(repo, reviews_csv)
print(f"Reviews saved to {reviews_csv}")
