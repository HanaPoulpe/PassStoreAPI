"""Blackbox testing for API list Password Files"""
import json
import unittest

import boto3patch as b3p
import unittest_extended as unittest2

# Import test target and map handler
import src.awslamda.PasswordFileList.lambda_handler as trg

handler = trg.lambda_handler


class LambdaPasswordFileList(unittest2.TestCase2):
    lambda_event_name = {
        "OK": "PasswordFileList",
        "Malformed": {"PasswordFileList-Malformed"}
    }

    def test_list_files_authorized(self):
        """Test call to API list Password Files"""
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
        ret = b3p.lambda_handler.start_lambda(
            handler,
            LambdaPasswordFileList.lambda_event_name["OK"]
        )

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
        expected_return = {
            "statusCode": int,
            "body": str
        }
        expected_body = {
            "status_code": int,
            "error_message": str,
        }
        ret = b3p.lambda_handler.start_lambda(
            handler,
            LambdaPasswordFileList.lambda_event_name["OK"]
        )

        self.assertTrue(True, "Lambda successful")
        self.assertDictStructure(expected_return, ret)
        self.assertEqual(403, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertEqual(403, ret_body["status_code"])

    def test_list_files_malformed_request(self):
        """Test call to API list Password Files with malformed request"""
        expected_return = {
            "statusCode": int,
            "body": str
        }
        expected_body = {
            "status_code": int,
            "error_message": str,
        }

        def run_test(event):
            """Tests factory"""
            self.assertTrue(True, f"Testing message: {event}")

            ret = b3p.lambda_handler.start_lambda(
                handler,
                event
            )

            self.assertTrue(True, "Lambda successful")
            self.assertDictStructure(expected_return, ret)
            self.assertEqual(400, ret["statusCode"])

            ret_body = json.loads(ret["body"])
            self.assertTrue(True, "Body is JSON Object")
            self.assertDictStructureStrict(expected_body, ret_body)
            self.assertEqual(400, ret_body["status_code"])

        for e in LambdaPasswordFileList.lambda_event_name["Malformed"]:
            run_test(e)


if __name__ == '__main__':
    unittest.main()
