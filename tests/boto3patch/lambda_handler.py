"""Basic lambda handler management"""
import dataclasses
import json
import time
import typing

LAMBDA_EVENT_PATH: str = "../lambda_events"


def load_event(event_name: str) -> typing.Dict[str, typing.Any]:
    """
    Load a lambda event from json file

    :param event_name: JSon file name
    :return: lambda event to send to the lambda handler
    """
    with open(f"{LAMBDA_EVENT_PATH}/{event_name}.json", "r") as fp:
        return json.load(fp)


@dataclasses.dataclass
class LambdaContext:
    """Basic lambda handler context"""
    @dataclasses.dataclass(frozen=True)
    class Identity:
        """Lambda Context Identity"""
        cognito_identity_id: typing.Optional[str] = None
        cognito_identity_pool_id: typing.Optional[str] = None

    @dataclasses.dataclass(frozen=True)
    class ClientContext:
        """Lambda Client context"""
        @dataclasses.dataclass(frozen=True)
        class Client:
            """Lambda client context client"""
            installation_id: typing.Optional[str] = "instid123456"
            app_title: typing.Optional[str] = "test_app"
            app_version_name: typing.Optional[str] = "1"
            app_version_code: typing.Optional[str] = "1.1"
            app_package_name: typing.Optional[str] = "test_package"

        custom: typing.Dict
        env: typing.Dict = None
        client: typing.Optional[Client] = Client()

    function_name: typing.Optional[str] = "test_lambda"
    function_version: typing.Optional[int] = 1
    invoked_function_arn: typing.Optional[str] = \
        "arn:aws:lambda:us-east-2:123456789012:function:test_lambda:1"
    memory_limit_in_mb: typing.Optional[int] = 128
    aws_request_id: typing.Optional[str] = "123456789abc"
    log_group_name: typing.Optional[str] = "lambda/test_lambda"
    log_stream_name: typing.Optional[str] = "123456789abc"
    identity: typing.Optional[Identity] = None
    client_context: typing.Optional[ClientContext] = None

    time_out: typing.Optional[int] = 900
    start_time: typing.Optional[int] = 0

    def get_remaining_time_in_millis(self) -> int:
        """Return lambda remaining time in ms"""
        return int(self.time_out - (time.time_ns() / 1000000 - self.start_time))


class LambdaTimeoutException(RuntimeError):
    """Lambda timeout error"""
    def __init__(self, *args):
        super(LambdaTimeoutException, self).__init__("Lambda execution time exceed timeout", *args)


def start_lambda(lambda_handler: typing.Callable, lambda_event_name: str,
                 lambda_context: typing.Optional[LambdaContext] = None) -> typing.Dict:
    """Runs a lambda"""
    event = load_event(lambda_event_name)
    if not lambda_context:
        lambda_context = LambdaContext()

    lambda_context.start_time = time.time_ns() / 1000000
    r = lambda_handler(event, lambda_context)
    if time.time_ns() / 1000000 - lambda_context.start_time >= lambda_context.time_out:
        raise LambdaTimeoutException()
    return r
