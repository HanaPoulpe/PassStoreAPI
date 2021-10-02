"""Unit Test for AWS Lambda Password File Get"""
import base64
import dateutil.parser
import json

import unittest_extended as unittest

# Import test target and map handler
import awslamda.PasswordFileGet.lambda_handler as trg
handler = trg.lambda_handler


class LambdaPasswordFileGet(unittest.TestCase2):
    def test_get_file_authorized(self):
        """Test call to API GET to an authorized file"""
        lambda_event = {
            "file_name": "user/mock/file",
            "user_id": "mockuser"
        }
        expected_return = {
            "statusCode": int,
            "body": str
        }
        expected_body = {
            "file_name": str,
            "status_code": int,
            "owner_id": str,
            "last_updated": str,
            "version_id": str,
            "checksum": str,
            "content": str
        }
        ret = handler(lambda_event, None)

        self.assertTrue(True, "Lambda successful")
        self.assertDictStructure(expected_return, ret)
        self.assertEqual(200, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertTrue(dateutil.parser.parse(ret_body["last_updated"]), "last_update is datetime")
        self.assertTrue(base64.b64decode(
            ret_body["checksum"]
        ), "checksum is b64 encoded")
        self.assertTrue(base64.b64decode(
            ret_body["content"]
        ))
        self.assertEqual(200, ret_body["status_code"])

    def test_get_file_access_denied(self):
        """Test call to API GET to an unauthorized file"""
        lambda_event = {
            "file_name": "user/mock/file",
            "user_id": "mockuser"
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

    def test_get_file_access_not_found(self):
        """Test call to API GET to a missing authorized file"""
        lambda_event = {
            "file_name": "user/mock/file",
            "user_id": "mockuser"
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
        self.assertEqual(404, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertEqual(404, ret_body["status_code"])


if __name__ == '__main__':
    unittest.main()
