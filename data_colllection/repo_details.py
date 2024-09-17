import csv

def save_commits_to_csv(repo, csv_file):
    """Save repository commits to a CSV file."""
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Commit SHA", "Author", "Email", "Date", "Message"])
        for commit in repo.get_commits()[:500]:
            writer.writerow([commit.sha, commit.commit.author.name, 
                             commit.commit.author.email, commit.commit.author.date, 
                             commit.commit.message])

def save_pull_requests_to_csv(repo, csv_file):
    """Save repository pull requests to a CSV file."""
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["PR Number", "Title", "Author", "Created At", "State"])
        for pr in repo.get_pulls()[:500]:
            writer.writerow([pr.number, pr.title, pr.user.login, pr.created_at, pr.state])

def save_issues_to_csv(repo, csv_file):
    """Save repository issues to a CSV file."""
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Issue Number", "Title", "Author", "Created At", "State", "Labels"])
        for issue in repo.get_issues()[:500]:
            labels = ', '.join([label.name for label in issue.labels])
            writer.writerow([issue.number, issue.title, issue.user.login, issue.created_at, issue.state, labels])

def save_reviews_to_csv(repo, csv_file):
    """Save repository pull request reviews to a CSV file."""
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["PR Number", "Review Author", "Review State", "Submitted At", "Review Body"])
        for pr in repo.get_pulls()[:500]:
            for review in pr.get_reviews():
                writer.writerow([pr.number, review.user.login, review.state, review.submitted_at, review.body])
