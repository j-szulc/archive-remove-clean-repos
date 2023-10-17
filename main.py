# Use at your own risk.

import os
import shutil
import sys

import click
import subprocess as sp

def clean_repo(path):

    def action_manual():
        if click.confirm("Repo is not clean do you want to clean it up manually?"):
            sp.run(["zsh"], cwd=path)

    def action_backup():
        if click.confirm('Repo is not clean. Push a commit "backup" and continue?'):
            sp.run(['git', 'add', '.'], cwd=path)
            sp.run(["git", "commit", "-m", "backup"], cwd=path)
            sp.run(['git', 'push'], cwd=path)

    def action_delete():
        if repo_clean():
            prompt = f'Repo is clean. Do you want to delete: {path}?'
        else:
            prompt = f'Repo is not clean. Do you want to delete {path} anyway?'
        if click.confirm(prompt):
            shutil.rmtree(path)

    def repo_clean():
        return not sp.check_output(['git', 'status', '--porcelain'], cwd=path)

    for action in [action_manual, action_backup, action_delete]:
        if action != action_delete and repo_clean():
            break
        sp.run(["git", "status"], cwd=path)
        sp.run(["git", "remote", "get-url", "--all", "origin"], cwd=path)
        if shutil.which("dust") is not None:
            sp.run(["dust", "-v", ".git"], cwd=path)
        action()


@click.command()
@click.argument("path")
def remove_uptodate_git_repos(path):
    if not os.path.isdir(path):
        raise click.ClickException("Path is not a directory")
    for folder in os.listdir(path):
        if not os.path.isdir(os.path.join(path, folder)):
            continue
        if not os.path.isdir(os.path.join(path, folder, '.git')):
            print(f"Warning: {folder} is not a git repo", file=sys.stderr)
            continue
        clean_repo(os.path.join(path, folder))

if __name__ == '__main__':
    remove_uptodate_git_repos()
