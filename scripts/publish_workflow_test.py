import unittest
from unittest.mock import patch

import publish_workflow as workflow


class WorkflowTests(unittest.TestCase):
    def test_selection_rejects_unsafe_empty_missing_and_duplicate_paths(self):
        for value in ['', '../jobs/a.json', 'jobs/../a.json', 'jobs/*.json',
                      'jobs/a.json;echo', 'jobs/not-a-real-record.json']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                workflow.select_files(value)
        name = str(next((workflow.ROOT / 'jobs').glob('*.json')).relative_to(workflow.ROOT))
        self.assertEqual(workflow.select_files(name), [name])
        with self.assertRaises(ValueError):
            workflow.select_files(f'{name}\n{name}')

    def test_preview_never_adds_apply(self):
        with patch.object(workflow, 'select_files', return_value=['jobs/example.json']), \
             patch.dict(workflow.os.environ, {'GITHUB_REPOSITORY': 'test/jobs', 'APPLY': 'false'}), \
             patch.object(workflow.subprocess, 'run') as run:
            workflow.main()
        self.assertEqual(run.call_count, 2)
        self.assertTrue(all('--apply' not in call.args[0] for call in run.call_args_list))

    def test_failed_preview_prevents_label_and_issue_writes(self):
        with patch.object(workflow, 'select_files', return_value=['jobs/example.json']), \
             patch.dict(workflow.os.environ, {'GITHUB_REPOSITORY': 'test/jobs', 'APPLY': 'true'}), \
             patch.object(workflow.subprocess, 'run', side_effect=[None, RuntimeError('invalid age')]) as run:
            with self.assertRaises(RuntimeError):
                workflow.main()
        self.assertEqual(run.call_count, 2)
