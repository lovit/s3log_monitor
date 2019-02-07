from config import bucket
from config import directory
from config import prefix
from config import ignore_ips
from datetime import datetime
from datetime import timedelta
from parser import LogStream
import os


def datetime_parse(dt):
    dt = datetime.strptime(dt, '%d/%b/%Y:%H:%M:%S')
    dt += timedelta(hours=9)
    return dt

def listup():
    command = 'aws s3 sync s3://{}/ {}'.format(bucket, directory)
    os.system(command)

    log_stream = LogStream(directory, prefix)
    logs = []
    for log in log_stream:
        if log.remote_ip in ignore_ips:
            continue
        cols = (datetime_parse(log.time.split()[0]), log.remote_ip, log.request_url.split('?')[0], log.bytes_sent)
        logs.append(cols)
    logs = sorted(logs, key=lambda x:x[0], reverse=True)

    def as_str(row):
        return '\t'.join(str(c) for c in row)

    logs_str = [as_str(row) for row in logs]
    return logs_str
    