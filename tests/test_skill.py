import importlib.util
import pathlib
import subprocess
import unittest
from unittest.mock import patch, MagicMock
path=pathlib.Path('skills/ebay-data/scripts/soldfetch_api.py')
spec=importlib.util.spec_from_file_location('helper',path);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
class SkillTests(unittest.TestCase):
    def test_invalid_inputs_do_not_send(self):
        for args in [['search','--keyword','sony','--count','201'],['search'],['item','--item-id','../usage'],['category','--category-id','0']]:
            result=subprocess.run(['python3',str(path),*args],capture_output=True,text=True)
            self.assertEqual(result.returncode,2)
    def test_rejects_arbitrary_path(self):
        with self.assertRaises(ValueError):helper.get('//evil.example',key='test-only')
    def test_request_parameters(self):
        opener=MagicMock();opener.open.return_value.__enter__.return_value.read.return_value=b'{}'
        with patch('urllib.request.build_opener',return_value=opener):helper.get('/v1/scrape',{'sold':False,'keyword':'a & b'},key='test-only',idempotency_key='stable')
        req=opener.open.call_args.args[0];self.assertIn('sold=false',req.full_url);self.assertNotIn('test-only',req.full_url);self.assertEqual(req.get_header('Idempotency-key'),'stable')
if __name__=='__main__':unittest.main()
