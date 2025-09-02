from github import Github, GithubException


class GitHubService:
    def __init__(self, token, repo_name):
        self.g = Github(token)
        self.repo = self.g.get_repo(repo_name)

    def create_branch(self, branch_name, source_branch="main"):
        sb = self.repo.get_branch(source_branch)
        self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=sb.commit.sha)
        print(f"Branch created: {branch_name}")

    def push_file(self, branch_name, file_path, content, commit_message="Update file"):
        try:
            file = self.repo.get_contents(file_path, ref=branch_name)
            self.repo.update_file(
                file.path, commit_message, content, file.sha, branch=branch_name
            )
        except GithubException:
            self.repo.create_file(
                file_path, commit_message, content, branch=branch_name
            )
        print(f"File pushed: {file_path}")

    def create_pull_request(self, title, body, branch_name, base="main"):
        pr = self.repo.create_pull(title=title, body=body, head=branch_name, base=base)
        print(f"PR created: {title}")
        return pr
