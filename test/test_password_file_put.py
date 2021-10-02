"""Blackbox testing for API Put Password File"""
import base64
import dateutil.parser
import json

import unittest_extended as unittest

# Import test target and map handler
import awslamda.PasswordFilePut.lambda_handler as trg
handler = trg.lambda_handler


class LambdaPasswordFilePut(unittest.TestCase2):
    def test_put_file_authorized(self):
        """Test call to API PUT an authorized file"""
        lambda_event = {
            "file_name": "user/mock/file",
            "user_id": "mockuser",
            "file_content": base64.b64encode(b"123456789azerty"),
            "checksum": b"123456789",
            "last_version_id": "123456789",
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
        }
        ret = handler(lambda_event, None)

        self.assertTrue(True, "Lambda successful")
        self.assertDictStructure(expected_return, ret)
        self.assertEqual(200, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertTrue(dateutil.parser.parse(ret_body["last_updated"]), "last_update is datetime")
        self.assertEqual(200, ret_body["status_code"])

    def test_put_file_access_denied(self):
        """Test call to API PUT an unauthorized file"""
        lambda_event = {
            "file_name": "user/mock/file",
            "user_id": "mockuser",
            "file_content": base64.b64encode(b"123456789azerty"),
            "checksum": b"123456789"
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

    def test_put_file_access_version_conflict(self):
        """Test call to API PUT an authorized file that have been change"""
        lambda_event = {
            "file_name": "user/mock/file",
            "user_id": "mockuser",
            "file_content": base64.b64encode(b"123456789azerty"),
            "checksum": b"123456789",
            "last_version_id": "123456789",
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
        self.assertEqual(428, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertEqual(428, ret_body["status_code"])

    def test_put_file_access_wrong_checksum(self):
        """Test call to API PUT a file with a wrong checksum"""
        lambda_event = {
            "file_name": "user/mock/file",
            "user_id": "mockuser",
            "file_content": base64.b64encode(b"123456789azerty"),
            "checksum": b"123456789",
            "last_version_id": "123456789",
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
        self.assertEqual(400, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertEqual(400, ret_body["status_code"])


if __name__ == '__main__':
    unittest.main()
