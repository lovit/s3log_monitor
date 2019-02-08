from bokeh.embed import file_html
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn, DateFormatter
from bokeh.resources import CDN
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

def byte_format(size):
    if size == '-':
        return size
    unit = 'Byte'
    if size > 1024:
        size /= 1024
        unit = 'KB'
    if size > 1024:
        size /= 1024
        unit = 'MB'
    size = int(size)
    return '{} {}'.format(size, unit)

def listup():
    command = 'aws s3 sync s3://{}/ {}'.format(bucket, directory)
    os.system(command)

    log_stream = LogStream(directory, prefix)
    logs = []
    for log in log_stream:
        if log.remote_ip in ignore_ips:
            continue
        cols = (datetime_parse(log.time.split()[0]),
                log.remote_ip,
                log.request_url.split('?')[0],
                byte_format(log.bytes_sent)
               )
        logs.append(cols)
    logs = sorted(logs, key=lambda x:x[0], reverse=True)

    if not logs:
        return 'Empty'

    return log_to_bokeh_widget(logs)

def log_to_str_list(logs):
    def as_str(row):
        return '\t'.join(str(c) for c in row)

    logs_str = [as_str(row) for row in logs]
    return logs_str

def log_to_bokeh_widget(logs):
    datetimes, ips, requests, bytes_ = zip(*logs)

    data = dict(
        datetimes = [str(c) for c in datetimes],
        ips = ips,
        requests = requests,
        bytes = bytes_
    )
    source = ColumnDataSource(data)

    columns = [
        TableColumn(field="datetimes", title="Datetime"),
        TableColumn(field="ips", title="Access IP"),
        TableColumn(field="requests", title="Request URL"),
        TableColumn(field="bytes", title="Bytes"),
    ]

    data_table = DataTable(source=source, columns=columns, width=1200, height=800)
    return file_html(data_table, CDN, "S3 Access Logs").strip()