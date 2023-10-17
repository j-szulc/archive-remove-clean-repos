# Use at your own risk.

import os
import shutil
import sys

import click
import subprocess as sp

def dry_remove(path, remove=False):
    if os.path.exists(path):
        prompt = "Would remove " if not remove else "Removing "
        print(prompt + path)
        if remove:
            sp.run(["rm", "-rf", path])

def clean_repo(path, remove):

    def action_manual():
        if click.confirm("Repo is not clean do you want to clean it up manually?"):
            sp.run(["zsh"], cwd=path)

    def action_backup():
        if click.confirm('Repo is not clean. Push a commit "backup" and continue?'):
            sp.run(['git', 'add', '.'], cwd=path)
            sp.run(["git", "commit", "-m", "backup"], cwd=path)
            sp.run(['git', 'push'], cwd=path)

    repo_clean_override = False

    def action_override():
        if click.confirm('Repo is not clean. Do you want to delete it anyway?'):
            repo_clean_override = True

    def repo_clean():
        return repo_clean_override or not sp.check_output(['git', 'status', '--porcelain'], cwd=path)

    for action in [action_manual, action_backup, action_override]:
        if repo_clean():
            break
        sp.run(["git", "status"], cwd=path)
        sp.run(["git", "remote", "get-url", "--all", "origin"], cwd=path)
        if shutil.which("dust") is not None:
            sp.run(["dust", "-v", ".git"], cwd=path)
        action()

    if repo_clean():
        dry_remove(path, remove)


@click.command()
@click.argument("path")
@click.option("--remove", "-r", is_flag=True, help="Do not perform a dry run.")
def remove_uptodate_git_repos(path, remove=False):
    if not os.path.isdir(path):
        raise click.ClickException("Path is not a directory")
    for folder in os.listdir(path):
        if not os.path.isdir(os.path.join(path, folder)):
            continue
        if not os.path.isdir(os.path.join(path, folder, '.git')):
            print(f"Warning: {folder} is not a git repo", file=sys.stderr)
            continue
        clean_repo(os.path.join(path, folder), remove)

if __name__ == '__main__':
    remove_uptodate_git_repos()
