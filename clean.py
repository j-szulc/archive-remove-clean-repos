import os
import shutil

import click
import subprocess as sp

default_trash = [
    '.DS_Store',
    '.localized',
    'Thumbs.db',
    'desktop.ini',
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
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

@click.command()
@click.argument("path")
@click.option("--remove", "-r", is_flag=True, help="Do not perform a dry run. (Default: False)")
def clean_repos(path, remove=False):
    for folder in os.listdir(path):
        if not os.path.isdir(os.path.join(path, folder)):
            continue
        if not os.path.isdir(os.path.join(path, folder, '.git')):
            continue
        for trash in default_trash:
            dry_remove(os.path.join(path, folder, trash), remove)

if __name__ == '__main__':
    clean_repos()
