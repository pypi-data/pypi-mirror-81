# -*- coding: utf-8 -*-
import base64
import hashlib
import re
import subprocess
import tempfile
import textwrap

import requests

import logging

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def clean_xml(xml):
    return re.sub(r'\s+(?=[<>])', '', xml).strip()


def remove_namespaces(xml):
    return re.sub(r'[souh]:', '', xml)


def prepare_template(template, data):
    template_clean = clean_xml(template)
    final_template = template_clean.format(**data)
    if 'signature' in data.keys() and not data.get('signature'):
        data['signature'] = '{signature}'
        template_signature_to_replace = template_clean.format(**data)
        return (final_template, template_signature_to_replace)
    return final_template


def prepare_binary(binary: bytes) -> str:
    '''Takes a bytes object an returns the string represents it'''
    return base64.encodebytes(binary).decode('UTF-8')


def digest(data: str) -> str:
    return prepare_binary(hashlib.sha1(data.encode('UTF-8')).digest())


def der_to_pem(der_data, type):
    wrapped = '\n'.join(textwrap.wrap(der_data, 64))
    pem = f"-----BEGIN {type}-----\n{wrapped}\n-----END {type}-----\n"
    return pem


def consume(soap_action, uri, body, token=None):
    headers = {
        'Content-type': 'text/xml; charset="utf-8"',
        'Accept': 'text/xml',
        'Cache-Control': 'no-cache',
        'SOAPAction': soap_action,
    }
    if token:
        headers['Authorization'] = f'WRAP access_token="{token}"'
    response = requests.post(uri, body, headers=headers)
    return response
