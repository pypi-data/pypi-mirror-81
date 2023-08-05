import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

__version__ = '0.0.1'


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        # Add any AWS Lambda events or context objects here
        self.aws_request_id = kwargs.pop('aws_request_id', '')
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
        log_record['schema_version'] = __version__
        if self.aws_request_id:
            log_record['aws_request_id'] = self.aws_request_id


def setup(*args, **kwargs):
    logger = logging.getLogger()
    # Remove Lambda Handler
    if len(logger.handlers) == 1:
        logger.removeHandler(logger.handlers[0])
    jsonHandler = logging.StreamHandler()
    formatter = CustomJsonFormatter(fmt='%(timestamp)s %(level)s %(name)s %(message)s', **kwargs)
    jsonHandler.setFormatter(formatter)
    logger.addHandler(jsonHandler)
