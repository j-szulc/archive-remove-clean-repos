# TODO - not fully working yet, use at your own risk

import os
import shutil

import click
import subprocess as sp

trash_files = [
    '.DS_Store',
    '.localized',
    'Thumbs.db',
    'desktop.ini',
]

trash_folders = [
    '__pycache__',
    '.ipynb_checkpoints',
    '.idea',
    '.vscode'
]

def dry_remove(path, remove=False):
    if os.path.exists(path):
        prompt = "Would remove " if not remove else "Removing "
        print(prompt + path)
        if remove:
            sp.run(["git", "rm", path])

def clean_repo(path, remove=False, bfg=False):
    if bfg:
        if not remove:
            raise click.ClickException("BFG requires --remove")
        assert shutil.which("bfg") is not None, "BFG not installed!"
        sp.run([
            "bfg",
            "--delete-folders",
            ",".join(trash_folders),
            "--delete-files",
            ",".join(trash_files),
            "--no-blob-protection",
            path
        ])
        sp.run([
            "git",
            "reflog",
            "expire",
            "--expire=now",
            "--all"
        ], cwd=path)
        sp.run([
            "git",
            "gc",
            "--prune=now",
            "--aggressive"
        ], cwd=path)
    for trash in trash_files + trash_folders:
        dry_remove(os.path.join(path, trash), remove)
    if remove:
        sp.run(["git","reset"],cwd=path)

@click.command()
@click.argument("path")
@click.option("--remove", "-r", is_flag=True, help="Do not perform a dry run. (Default: False)")
@click.option("--bfg", "-b", is_flag=True, help="Use BFG to clean the repo. (Default: False)")
def clean_repos(path, remove=False, bfg=False):
    for folder in os.listdir(path):
        if not os.path.isdir(os.path.join(path, folder)):
            continue
        if not os.path.isdir(os.path.join(path, folder, '.git')):
            continue
        clean_repo(os.path.join(path, folder), remove, bfg)


if __name__ == '__main__':
    clean_repos()
