"""Blackbox testing for API Delete a Password File"""
import dateutil.parser
import json

import boto3patch as b3p
import unittest_extended as unittest

# Import test target and map handler
import src.awslamda.PasswordFileDelete.lambda_handler as trg

handler = trg.lambda_handler


class LambdaPasswordFileDelete(unittest.TestCase2):
    lambda_event_name = {
        "OK": "PasswordFileDelete",
        "Malformed": {
            "PasswordFileDelete-Malformed-JSon",
            "PasswordFileDelete-Malformed-UnexpectedMembers",
            "PasswordFileDelete-Malformed-MissingMember"
        }
    }

    def test_delete_file_authorized(self):
        """Test call to API delete an authorized file"""
        expected_return = {
            "statusCode": int,
            "body": str
        }
        expected_body = {
            "file_name": str,
            "status_code": int,
            "last_updated": str,
            "version_id": str,
            # NIY: "recovery_deadline": str
        }
        ret = b3p.lambda_handler.start_lambda(
            handler,
            LambdaPasswordFileDelete.lambda_event_name["OK"]
        )

        self.assertTrue(True, "Lambda successful")
        self.assertDictStructure(expected_return, ret)
        self.assertEqual(200, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertTrue(dateutil.parser.parse(ret_body["last_updated"]), "last_update is datetime")
        self.assertEqual(200, ret_body["status_code"])
        self.assertTrue(dateutil.parser.parse(ret_body["recovery_deadline"]),
                        "recovery_deadline is datetime")

    def test_delete_file_access_denied(self):
        """Test call to API delete an unauthorized file"""
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
            LambdaPasswordFileDelete.lambda_event_name["OK"]
        )

        self.assertTrue(True, "Lambda successful")
        self.assertDictStructure(expected_return, ret)
        self.assertEqual(403, ret["statusCode"])

        ret_body = json.loads(ret["body"])
        self.assertTrue(True, "Body is JSON Object")
        self.assertDictStructureStrict(expected_body, ret_body)
        self.assertEqual(403, ret_body["status_code"])

    def test_delete_files_malformed_request(self):
        """Test call to API delete Password Files with malformed request"""
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

        for e in LambdaPasswordFileDelete.lambda_event_name["Malformed"]:
            run_test(e)


if __name__ == '__main__':
    unittest.main()
