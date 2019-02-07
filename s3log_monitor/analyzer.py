from config import bucket
from config import directory
from config import prefix
from config import ignore_ips
from parser import LogStream
import os

def listup():

    command = 'aws s3 sync s3://{}/ {}'.format(bucket, directory)
    os.system(command)

    log_stream = LogStream(directory, prefix)
    logs_str = []
    for log in log_stream:
        if log.remote_ip in ignore_ips:
            continue
        cols = (log.time.split()[0], log.remote_ip, log.request_url.split('?')[0], log.bytes_sent)
        log_str = '\t'.join((str(c) for c in cols))
        logs_str.append(log_str)
    return logs_str
    