from github import Github


class GitHubService:
    def __init__(self, token, repo_name):
        self.client = Github(token)
        self.repo = self.client.get_repo(repo_name)

    def create_branch(self, branch_name, base_branch="main"):
        source = self.repo.get_branch(base_branch)
        self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
        print(f"Created branch {branch_name}")

    def push_file(self, branch_name, file_path, content, commit_message):
        try:
            existing_file = self.repo.get_contents(file_path, ref=branch_name)
            self.repo.update_file(
                existing_file.path,
                commit_message,
                content,
                existing_file.sha,
                branch=branch_name,
            )
            print(f"Updated file: {file_path}")
        except Exception:
            self.repo.create_file(
                file_path, commit_message, content, branch=branch_name
            )
            print(f"Created file: {file_path}")

    def create_pull_request(self, title, body, branch_name, base_branch="main"):
        pr = self.repo.create_pull(
            title=title, body=body, head=branch_name, base=base_branch
        )
        return pr
