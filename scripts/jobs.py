#!/usr/bin/env python3
"""Manage job forms, labels and issues using Python's standard library and gh."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import parse_qs, quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / '.github/job-catalog.json').read_text())
FORM = ROOT / '.github/ISSUE_TEMPLATE/job.yml'


def gh(*args, payload=None):
    command = ['gh', *args]
    if payload is None:
        return subprocess.check_output(command, cwd=ROOT, text=True)
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json') as body:
        json.dump(payload, body)
        body.flush()
        return subprocess.check_output(command + ['--input', body.name], cwd=ROOT, text=True)


def labels():
    return [dict(name=f"{group['id']}:{value}", color=group['color'], description=description)
            for group in CATALOG['groups'] for value, description in group['values'].items()]


def form_text():
    body = []
    for field in CATALOG['fields']:
        body.append(dict(type=field['type'], id=field['id'],
                         attributes=dict(label=field['label'], description=field['description']),
                         validations=dict(required=True)))
    for group in CATALOG['groups']:
        body.append(dict(type='dropdown', id=group['id'], attributes=dict(
            label=group['label'], description=group['description'], multiple=group['multiple'],
            options=list(group['values'])), validations=dict(required=True)))
    # JSON is a YAML subset, accepted by GitHub's issue form parser.
    return json.dumps(dict(name='Job opportunity', description='Share a verified job opportunity in English.',
                          title='[Company] Job Title — Location / Work arrangement', body=body), indent=2) + '\n'


def load_jobs(paths):
    records, sources, urls = [], set(), set()
    expected = {f['id'] for f in CATALOG['fields']} | {g['id'] for g in CATALOG['groups']}
    for path in paths:
        job = json.loads(path.read_text())
        if set(job) != expected:
            raise ValueError(f'{path}: fields differ: {set(job) ^ expected}')
        for field in CATALOG['fields']:
            value = job[field['id']]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f'{path}: {field["id"]} must be nonempty text')
            if field['type'] == 'input' and '\n' in value:
                raise ValueError(f'{path}: {field["id"]} must be one line')
        url = urlsplit(job['source_url'])
        if url.scheme != 'https' or not url.hostname or url.username or url.password or url.fragment:
            raise ValueError(f'{path}: invalid public HTTPS URL')
        if any(k.lower().startswith(('utm_', 'gh_src')) or k.lower() in {'token', 'access_token', 'api_key'} for k in parse_qs(url.query)):
            raise ValueError(f'{path}: use a clean source URL without tracking or tokens')
        if not re.fullmatch(r'[a-z0-9][a-z0-9:._-]+', job['source_key']):
            raise ValueError(f'{path}: invalid source_key')
        checked = date.fromisoformat(job['last_checked'])
        if checked > date.today():
            raise ValueError(f'{path}: verification date is in the future')
        selected = []
        for group in CATALOG['groups']:
            values = job[group['id']]
            if not isinstance(values, list) or not values or len(set(values)) != len(values):
                raise ValueError(f'{path}: {group["id"]} must be a nonempty unique list')
            if not group['multiple'] and len(values) != 1:
                raise ValueError(f'{path}: {group["id"]} accepts one value')
            if 'unspecified' in values and len(values) > 1:
                raise ValueError(f'{path}: unspecified cannot accompany known values')
            for value in values:
                if value not in group['values']:
                    raise ValueError(f'{path}: unknown {group["id"]}: {value}')
                selected.append(f'{group["id"]}:{value}')
        if job['source_key'] in sources or job['source_url'] in urls:
            raise ValueError(f'{path}: duplicate source in local records')
        sources.add(job['source_key'])
        urls.add(job['source_url'])
        title = f"[{job['company']}] {job['job_title']} — {job['location']} / {job['work'][0].replace('-', ' ').title()}"
        content = [f"<!-- job-source: {job['source_key']} -->"]
        for field in CATALOG['fields']:
            content.extend([f"## {field['label']}", job[field['id']]])
        content.append('## Classification')
        content.extend(f"- {g['label']}: {', '.join(job[g['id']])}" for g in CATALOG['groups'])
        records.append(dict(title=title, body='\n\n'.join(content) + '\n', labels=selected, job=job))
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'generate', 'labels', 'publish'])
    parser.add_argument('files', nargs='*', type=Path, help='Job JSON files; default: jobs/*.json')
    parser.add_argument('--apply', action='store_true', help='Apply labels or create missing issues')
    parser.add_argument('--repo', help='owner/name; defaults to this checkout repository')
    args = parser.parse_args()
    records = load_jobs(args.files or sorted((ROOT / 'jobs').glob('*.json')))
    if args.command == 'generate':
        FORM.write_text(form_text())
        print(f'Generated {FORM.relative_to(ROOT)}')
        return
    if FORM.read_text() != form_text():
        raise ValueError('Issue form is stale; run python3 scripts/jobs.py generate')
    if args.command == 'check':
        print(f'Validated {len(records)} jobs, {len(labels())} labels and generated form.')
        return
    repo = args.repo or gh('repo', 'view', '--json', 'nameWithOwner', '--jq', '.nameWithOwner').strip()
    if not re.fullmatch(r'[\w.-]+/[\w.-]+', repo):
        raise ValueError('Invalid repository name')
    print(f'Repository: {repo}')
    prefix = f'repos/{repo}'
    existing_labels = {x['name']: x for page in json.loads(gh('api', '--paginate', '--slurp',
                       f'{prefix}/labels?per_page=100')) for x in page}
    if args.command == 'labels':
        for desired in labels():
            current = existing_labels.get(desired['name'])
            if current and all(current.get(k) == v for k, v in desired.items()):
                continue
            action = 'update' if current else 'create'
            print(f'{action}: {desired["name"]}')
            if args.apply:
                endpoint = f"{prefix}/labels" + (f"/{quote(desired['name'], safe='')}" if current else '')
                gh('api', '--method', 'PATCH' if current else 'POST', endpoint, payload=desired)
        return
    issues = [x for page in json.loads(gh('api', '--paginate', '--slurp',
              f'{prefix}/issues?state=all&per_page=100')) for x in page if 'pull_request' not in x]
    missing = {label for r in records for label in r['labels']} - existing_labels.keys()
    if args.apply and missing:
        raise ValueError(f'Sync labels first; missing: {sorted(missing)}')
    for record in records:
        marker = f"<!-- job-source: {record['job']['source_key']} -->"
        matches = [i for i in issues if marker in (i['body'] or '') or record['job']['source_url'] in (i['body'] or '')]
        if matches:
            print('Skip existing: ' + ', '.join(i['html_url'] for i in matches))
            continue
        print(f"Create: {record['title']}\nLabels: {', '.join(record['labels'])}")
        if args.apply:
            result = json.loads(gh('api', '--method', 'POST', f'{prefix}/issues', payload={
                k: record[k] for k in ['title', 'body', 'labels']}))
            issues.append(result)
            print(result['html_url'])
        else:
            print(record['body'])


if __name__ == '__main__':
    main()
