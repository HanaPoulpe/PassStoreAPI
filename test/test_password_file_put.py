"""Blackbox testing for API Put Password File"""
import base64
import dateutil.parser
import json

import boto3patch as b3p
import unittest_extended as unittest

# Import test target and map handler
import src.awslamda.PasswordFilePut.lambda_handler as trg
handler = trg.lambda_handler


class LambdaPasswordFilePut(unittest.TestCase2):
    lambda_event_name = {
        "OK": "PasswordFilePut",
        "Malformed": {
            "PasswordFilePut-Malformed-JSon",
            "PasswordFilePut-Malformed-UnexpectedMembers",
            "PasswordFilePut-Malformed-MissingMember",
            "PasswordFilePut-Malformed-InvalidChecksum",
            "PasswordFilePut-Malformed-WrongChecksum",
        }
    }

    def test_put_file_authorized(self):
        """Test call to API PUT an authorized file"""
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
        ret = b3p.lambda_handler.start_lambda(
            handler,
            LambdaPasswordFilePut.lambda_event_name["OK"]
        )

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
        expected_return = {
            "statusCode": int,
            "body": str
        }
        expected_body = {
            "file_name": str,
            "status_code": int,
            "error_message": str,
        }
        ret = b3p.lambda_handler.start_lambda(
            handler,
            LambdaPasswordFilePut.lambda_event_name["OK"]
        )

        self.assertTrue(True, "Lambda successful")
        self.assertDictStructure(expected_return, ret)
        self.assertEqual(403, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertEqual(403, ret_body["status_code"])

    def test_put_file_access_version_conflict(self):
        """Test call to API PUT an authorized file that have been change"""
        expected_return = {
            "statusCode": int,
            "body": str
        }
        expected_body = {
            "file_name": str,
            "status_code": int,
            "error_message": str,
        }
        ret = b3p.lambda_handler.start_lambda(
            handler,
            LambdaPasswordFilePut.lambda_event_name["OK"]
        )

        self.assertTrue(True, "Lambda successful")
        self.assertDictStructure(expected_return, ret)
        self.assertEqual(428, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertEqual(428, ret_body["status_code"])

    def test_list_files_malformed_request(self):
        """Test call to API put Password Files with malformed request"""
        expected_return = {
            "statusCode": int,
            "body": str
        }
        expected_body = {
            "file_name": str,
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

        for e in LambdaPasswordFilePut.lambda_event_name["Malformed"]:
            run_test(e)


if __name__ == '__main__':
    unittest.main()
