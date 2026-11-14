"""Exercise publication behavior with a temporary GitHub CLI substitute."""
import json
from datetime import date, timedelta
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FAKE_GH = '''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
p = Path(os.environ['JOBS_TEST_STATE'])
s = json.loads(p.read_text())
endpoint = next(a for a in args if a.startswith('repos/'))
method = args[args.index('--method')+1] if '--method' in args else 'GET'
payload = json.loads(Path(args[args.index('--input')+1]).read_text()) if '--input' in args else None
if method == 'GET':
    print(json.dumps([s['labels'] if '/labels' in endpoint else s['issues']]))
else:
    s['writes'] += 1
    if '/labels' in endpoint:
        if method == 'PATCH':
            s['labels'] = [payload if x['name'] == payload['name'] else x for x in s['labels']]
        else:
            s['labels'].append(payload)
        result = payload
    else:
        result = dict(payload, number=len(s['issues'])+1, html_url='https://github.com/test/jobs/issues/'+str(len(s['issues'])+1), state='open')
        s['issues'].append(result)
    p.write_text(json.dumps(s))
    print(json.dumps(result))
'''


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.state_path = self.folder / 'state.json'
        self.state_path.write_text(json.dumps(dict(labels=[], issues=[], writes=0)))
        fake = self.folder / 'gh'
        fake.write_text(FAKE_GH)
        fake.chmod(0o755)
        self.env = dict(os.environ, PATH=f'{self.folder}{os.pathsep}{os.environ["PATH"]}',
                        JOBS_TEST_STATE=str(self.state_path))

    def run_cli(self, command, *args, success=True):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/jobs.py'), command,
                                 *map(str, args), '--repo', 'test/jobs'], env=self.env,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def state(self):
        return json.loads(self.state_path.read_text())

    def test_preview_never_writes_and_label_sync_is_idempotent(self):
        self.run_cli('labels')
        self.run_cli('publish')
        self.assertEqual(self.state()['writes'], 0)
        self.run_cli('labels', '--apply')
        state = self.state()
        count = state['writes']
        state['labels'].append(dict(name='custom', color='ffffff', description='Keep me'))
        self.state_path.write_text(json.dumps(state))
        self.run_cli('labels', '--apply')
        self.assertEqual(self.state()['writes'], count)
        self.assertIn('custom', [x['name'] for x in self.state()['labels']])

    def test_publish_skips_open_and_closed_issues(self):
        self.run_cli('labels', '--apply')
        self.run_cli('publish', '--apply')
        state = self.state()
        expected = len(list((ROOT / 'jobs').glob('*.json')))
        self.assertEqual(len(state['issues']), expected)
        self.assertTrue(all(x['labels'] for x in state['issues']))
        count = state['writes']
        state['issues'][0]['state'] = 'closed'
        self.state_path.write_text(json.dumps(state))
        self.run_cli('publish', '--apply')
        self.assertEqual(self.state()['writes'], count)
        self.assertEqual(self.state()['issues'][0]['state'], 'closed')

    def test_recent_filter_uses_original_date_and_rejects_unknown_dates(self):
        job = json.loads(next((ROOT / 'jobs').glob('*.json')).read_text())
        job['last_checked'] = date.today().isoformat()
        selected = self.folder / 'recent.json'
        for days in [7, 8, None]:
            with self.subTest(days=days):
                if days is None:
                    job.pop('published_on', None)
                else:
                    job['published_on'] = (date.today() - timedelta(days=days)).isoformat()
                selected.write_text(json.dumps(job))
                self.run_cli('publish', selected, '--max-age-days', '7', success=days == 7)
                self.assertEqual(self.state()['writes'], 0)

    def test_missing_labels_prevent_any_issue_write(self):
        self.run_cli('publish', '--apply', success=False)
        self.assertEqual(self.state()['writes'], 0)

    def test_existing_manual_issue_is_detected_by_original_url(self):
        job_path = next((ROOT / 'jobs').glob('*.json'))
        job = json.loads(job_path.read_text())
        self.run_cli('labels', '--apply')
        state = self.state()
        state['issues'] = [dict(body=job['source_url'], html_url='https://github.com/test/jobs/issues/1', state='closed')]
        self.state_path.write_text(json.dumps(state))
        count = state['writes']
        self.run_cli('publish', job_path, '--apply')
        self.assertEqual(self.state()['writes'], count)


if __name__ == '__main__':
    unittest.main()
