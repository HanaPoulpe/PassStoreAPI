"""Blackbox testing for API list Password Files"""
import base64
import dateutil.parser
import json

import unittest_extended as unittest

# Import test target and map handler
import awslamda.PasswordFileList.lambda_handler as trg

handler = trg.lambda_handler


class LambdaPasswordFileList(unittest.TestCase2):
    def test_list_files_authorized(self):
        """Test call to API list Password Files"""
        lambda_event = {
            "user_id": "mockuser",
        }
        expected_return = {
            "statusCode": int,
            "body": str
        }
        expected_body = {
            "status_code": int,
            "files": list,
        }
        expected_files_dict = {
            "file_name": str,
            "version_id": str,
            "last_updated": str,
            "owner_id": str,
            "access_level": str,
        }
        ret = handler(lambda_event, None)

        self.assertTrue(True, "Lambda successful")
        self.assertDictStructure(expected_return, ret)
        self.assertEqual(200, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertTrue(ret_body["files"], "files is not empty")
        [self.assertDictStructureStrict(expected_files_dict, f) for f in ret_body["files"]]

    def test_list_files_access_denied(self):
        """Test call to API list Password Files"""
        lambda_event = {
            "user_id": "mockuser",
        }
        expected_return = {
            "statusCode": int,
            "body": str
        }
        expected_body = {
            "file_name": str,
            "status_code": int,
            "error_message": str,
        }
        ret = handler(lambda_event, None)

        self.assertTrue(True, "Lambda successful")
        self.assertDictStructure(expected_return, ret)
        self.assertEqual(403, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertEqual(403, ret_body["status_code"])


if __name__ == '__main__':
    unittest.main()
