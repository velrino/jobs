#!/usr/bin/env python3
"""Run the manual Action through the existing publisher, with scoped inputs."""
import os
from pathlib import Path
import re
import subprocess
import sys

from jobs import ROOT


def select_files(value):
    names = value.split()
    if not names:
        raise ValueError('Select at least one committed jobs/NAME.json file')
    paths = []
    for name in names:
        if not re.fullmatch(r'jobs/[A-Za-z0-9_.-]+\.json', name):
            raise ValueError(f'Invalid job path: {name}')
        path = ROOT / name
        if path.is_symlink() or not path.is_file() or path.resolve().parent != ROOT / 'jobs':
            raise ValueError(f'Expected a regular job record: {name}')
        if name in paths:
            raise ValueError(f'Duplicate selection: {name}')
        paths.append(name)
    return paths


def main():
    paths = select_files(os.environ.get('JOB_FILES', ''))
    repo = os.environ['GITHUB_REPOSITORY']
    base = [sys.executable, str(ROOT / 'scripts/jobs.py')]
    publish = base + ['publish', *paths, '--repo', repo, '--max-age-days', '7']
    # Validate age and preview before the first possible write, including labels.
    subprocess.run(base + ['check'], cwd=ROOT, check=True)
    subprocess.run(publish, cwd=ROOT, check=True)
    if os.environ.get('APPLY') == 'true':
        subprocess.run(base + ['labels', '--repo', repo, '--apply'], cwd=ROOT, check=True)
        subprocess.run(publish + ['--apply'], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
