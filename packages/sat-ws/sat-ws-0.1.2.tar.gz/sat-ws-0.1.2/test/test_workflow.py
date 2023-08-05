# -*- coding: utf-8 -*-
import base64
import logging
from datetime import datetime

from ..sat_api import SAT

_logger = logging.getLogger(__name__)

CERT_FILE_PATH = 'fake-fiel/EKU9003173C9.cer'
KEY_FILE_PATH = 'fake-fiel/EKU9003173C9.key'
PASSWORD_PATH = 'fake-fiel/EKU9003173C9.txt'

try:
    cert = open(CERT_FILE_PATH, 'rb').read()
    key = open(KEY_FILE_PATH, 'rb').read()
    password = open(PASSWORD_PATH, 'r').read().encode('UTF-8')
except OSError:
    _logger.error('Error opening files')
    raise

sat = SAT(cert, key, password)
# sat.login()
query_id = sat.query(datetime.fromisoformat('2020-09-01'), datetime.fromisoformat('2020-09-24T23:59:58'), SAT.DownloadType.RECEIVED, SAT.RequestType.CFDI)
packages = sat.wait_query(query_id)
downloads = sat.download(packages)
for id, content in downloads.items():
    with open(f'{id}.zip', 'wb') as of:
        of.write(content)
print('Done')
