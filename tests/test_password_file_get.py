"""Unit Test for AWS Lambda Password File Get"""
import base64
import dateutil.parser
import json
import unittest

import boto3patch as b3p
import unittest_extended as unittest2

# Import test target and map handler
import src.awslamda.PasswordFileGet.lambda_handler as trg
handler = trg.lambda_handler


class LambdaPasswordFileGet(unittest2.TestCase2):
    lambda_event_name = {
        "OK": "PasswordFileGet",
        "Malformed": {
            "PasswordFileGet-Malformed-JSon",
            "PasswordFileGet-Malformed-UnexpectedMembers",
            "PasswordFileGet-Malformed-MissingMembers"
        }
    }

    def test_get_file_authorized(self):
        """Test call to API GET to an authorized file"""
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
        ret = b3p.lambda_handler.start_lambda(
            handler,
            LambdaPasswordFileGet.lambda_event_name["OK"]
        )

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
            LambdaPasswordFileGet.lambda_event_name["OK"]
        )

        self.assertTrue(True, "Lambda successful")
        self.assertDictStructure(expected_return, ret)
        self.assertEqual(403, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertEqual(403, ret_body["status_code"])

    def test_get_file_access_not_found(self):
        """Test call to API GET to a missing authorized file"""
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
            LambdaPasswordFileGet.lambda_event_name["OK"]
        )

        self.assertTrue(True, "Lambda successful")
        self.assertDictStructure(expected_return, ret)
        self.assertEqual(404, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertEqual(404, ret_body["status_code"])

    def test_list_files_malformed_request(self):
        """Test call to API get Password Files with malformed request"""
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

        for e in LambdaPasswordFileGet.lambda_event_name["Malformed"]:
            run_test(e)


if __name__ == '__main__':
    unittest.main()
