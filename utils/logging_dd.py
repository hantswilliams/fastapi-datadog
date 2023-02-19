import logging
import sys
import os
from dotenv import load_dotenv
import json

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem

## load in the .env.dev file
load_dotenv('.env.dev')

# Set up the Datadog API client
config = Configuration()
config.api_key['DD-API-KEY'] = os.getenv("DD_API_KEY")
print('DD_API_KEY: ', os.getenv("DD_API_KEY"))
config.host = 'https://http-intake.logs.datadoghq.com'
api_client = ApiClient(configuration=config)
logs = LogsApi(api_client)

# Set up logging to file and terminal
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(filename="./app.log", mode="w"),
        logging.StreamHandler(sys.stdout)
    ]
)

# # Set up the logger for Uvicorn to use
# logger = logging.getLogger("uvicorn")
# logger.handlers = logging.getLogger().handlers
# logger.info('Starting the app logging...')

# Define a custom logging handler that sends logs to Datadog
class DatadogHandler(logging.Handler):
    def emit(self, record):
        # # Ignore debug messages
        # if record.levelno == logging.DEBUG:
        #     return

        # if record.getMessage() contains the word error, errors, or exception, set the log level to error
        if "error" in record.getMessage().lower() or "exception" in record.getMessage().lower():
            record.levelname = "ERROR"

        # if record.getMessage() contains any number between 400 and 599, set the log level to error
        if any(str(x) in record.getMessage() for x in range(400, 600)):
            record.levelname = "ERROR"


        toJson = json.dumps(
            {
                "python-logging": {
                    "py-env": os.getenv("DD_LOGGING_ENV"),
                    "py-message": record.getMessage(),
                    "py-status": record.levelname.lower(),
                    "py-logger": record.name,
                    "py-stacktrace": record.exc_info,
                    "py-exception": record.exc_text,
                    "py-line": record.lineno,
                    "py-file": record.filename,
                    "py-function": record.funcName,
                    "py-level": record.levelno,
                    "py-path": record.pathname,
                    "py-thread": record.thread,
                    "py-threadName": record.threadName,
                    "py-process": record.process,
                    "py-processName": record.processName,
                    "py-args": record.args,
                    "py-msecs": record.msecs,
                    "py-relativeCreated": record.relativeCreated,
                    "py-created": record.created,
                    "py-module": record.module,
                }
            }

        )

        # Send the log to Datadog using the Logs API
        try:
            body = HTTPLog(
                [
                    HTTPLogItem(
                        ddsource="Python",
                        ddtags="env:{}".format(os.getenv("DD_LOGGING_ENV")),
                        hostname="{}".format(os.getenv("DD_HOSTNAME")),
                        message= toJson,
                        service="{}".format(os.getenv("DD_SERVICE")),
                        status=record.levelname.lower()
                    ),
                ]
            )

            logs.submit_log(content_encoding=ContentEncoding.DEFLATE, body=body)
            # print(response)

        except Exception as e:
            print(f"Error sending log to Datadog: {e}")


# Set up the logger for Uvicorn to use
logger = logging.getLogger("uvicorn")
# logger.handlers = logging.getLogger().handlers
logger.info('Starting the app logging...')
logger.addHandler(DatadogHandler())