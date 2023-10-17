import os
import click
import subprocess as sp

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
            continue
        if sp.check_output(['git', 'status', '--porcelain'], cwd=os.path.join(path, folder)):
            continue
        prompt = "Would remove " if not remove else "Removing "
        print(prompt + os.path.join(path, folder))
        if remove:
            os.system('rm -rf ' + os.path.join(path, folder))

if __name__ == '__main__':
    remove_uptodate_git_repos()
