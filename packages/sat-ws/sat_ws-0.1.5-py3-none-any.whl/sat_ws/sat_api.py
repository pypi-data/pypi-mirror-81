# -*- coding: utf-8 -*-
import time
import hashlib
import json
import logging
from datetime import datetime, timedelta, timezone
from uuid import uuid1
from enum import Enum
import base64

import xmltodict
from OpenSSL import crypto

from . import utils

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


TEMPLATES = {
    'Envelope': open('templates/common/Envelope.xml', 'r').read(),
    'KeyInfo': open('templates/common/KeyInfo.xml', 'r').read(),
    'Signature': open('templates/common/Signature.xml', 'r').read(),
    'SignedInfo': open('templates/common/SignedInfo.xml', 'r').read(),
    'Timestamp': open('templates/login/Timestamp.xml', 'r').read(),
    'LoginEnvelope': open('templates/login/Envelope.xml', 'r').read(),
    'SolicitaDescarga': open('templates/query/SolicitaDescarga.xml', 'r').read(),
    'VerificaSolicitudDescarga': open('templates/verify/VerificaSolicitudDescarga.xml', 'r').read(),
    'PeticionDescargaMasivaTercerosEntrada': open('templates/download/PeticionDescargaMasivaTercerosEntrada.xml', 'r').read(),
}


def ensure_login(f):
    def wrapper(*args, **kwargs):
        self = args[0]
        self.login()
        res = f(*args, **kwargs)
        return res
    return wrapper


class SAT:
    '''Class to make a connection to the SAT'''

    class DownloadType:
        '''Helper to select the download type'''
        ISSUED = 'RfcEmisor'
        RECEIVED = 'RfcReceptor'

    class RequestType:
        '''Helper to select the request type'''
        CFDI = 'CFDI'
        METADATA = 'Metadata'

    cert = None
    key = None
    password = None
    key_pem = None
    cert_pem = None
    certificate = None
    rfc = None
    token = None
    token_expires = None

    def __init__(self, cert: bytes, key: bytes, password: str) -> None:
        '''Loads the certificate, key file and password to stablish the connection to the SAT'''
        self.cert = utils.prepare_binary(cert)
        self.key = utils.prepare_binary(key)
        self.password = password
        self._load_certs()
        self._compute_data_from_cert()
        _logger.info('Data correctly loaded')

    def _load_certs(self):
        '''Loads the PEM version of the certificate and key file, also loads the crypto certificate'''
        self.key_pem = utils.der_to_pem(self.key, type='ENCRYPTED PRIVATE KEY')
        self.cert_pem = utils.der_to_pem(self.cert, type='CERTIFICATE')
        self.certificate = crypto.load_certificate(crypto.FILETYPE_PEM, self.cert_pem)

    def _compute_data_from_cert(self):
        '''Gets the RFC and Issuer directly from the certificate'''
        self._get_rfc_from_cert()
        self._get_issuer_from_cert()

    def _get_rfc_from_cert(self):
        '''Gets the RFC from the certificate'''
        subject_components = self.certificate.get_subject().get_components()
        for c in subject_components:
            if c[0] == b'x500UniqueIdentifier':
                self.rfc = c[1].decode('UTF-8')
                _logger.debug(f'RFC {self.rfc} loaded')
                break
        else:
            raise Exception('No RFC foundend')

    def _get_issuer_from_cert(self):
        '''Gets the Issuer from the certificate'''
        self.certificate.issuer = ','.join([
            f'{c[0].decode("UTF-8")}={c[1].decode("UTF-8")}'
            for c in self.certificate.get_issuer().get_components()
        ])
        _logger.debug(f'Issuer {self.certificate.issuer} loaded')

    def _token_expired(self) -> None:
        '''Checks if the token expiration date is yet to come'''
        if not self.token or not self.token_expires:
            _logger.debug('Token expired')
            return True
        return self.token_expires > datetime.utcnow()

    def _create_common_envelope(self, template: str, data: dict) -> str:
        _logger.debug('Creating Envelope')
        _logger.debug(f'{template}')
        _logger.debug(f'{data}')
        query_data, query_data_signature = utils.prepare_template(template, data)
        digest_value = utils.digest(query_data)
        signed_info = utils.prepare_template(TEMPLATES['SignedInfo'], {
            'uri': '',
            'digest_value': digest_value,
        })
        key_info = utils.prepare_template(TEMPLATES['KeyInfo'], {
            'issuer_name': self.certificate.issuer,
            'serial_number': self.certificate.get_serial_number(),
            'certificate': self.cert,
        })
        signature_value = self.sign(signed_info)
        signature = utils.prepare_template(TEMPLATES['Signature'], {
            'signed_info': signed_info,
            'signature_value': signature_value,
            'key_info': key_info,
        })
        envelope_content = utils.prepare_template(query_data_signature, {
            'signature': signature,
        })
        envelope = utils.prepare_template(TEMPLATES['Envelope'], {
            'content': envelope_content,
        })
        _logger.debug('Final Envelope')
        _logger.debug(f'{envelope}')
        return envelope

    def sign(self, data) -> str:
        '''Signs the `data` using SHA1 with the `key_pem` content'''
        _logger.debug(f'Signing {data}')
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, self.key_pem, passphrase=self.password)
        signed_data = utils.prepare_binary(crypto.sign(private_key, data, 'sha1'))
        return signed_data

    def login(self):
        '''If the current token is invalid, tries to login'''
        if self._token_expired():
            _logger.debug('Token expired, creating a new one')
            self._login()
            _logger.debug('New token created')

    def _login(self):
        request_content = self._get_login_soap_body()
        response = utils.consume(
            'http://DescargaMasivaTerceros.gob.mx/IAutenticacion/Autentica',
            'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/Autenticacion/Autenticacion.svc',
            request_content,
        )
        if response.status_code != 200:
            raise Exception(response.reason)
        else:
            self._get_login_data(utils.remove_namespaces(response.content.decode('UTF-8')))

    def _get_login_soap_body(self):
        created = datetime.utcnow()
        expires = created + timedelta(minutes=5)
        self.token_expires = expires
        created = created.isoformat()
        expires = expires.isoformat()
        timestamp = utils.prepare_template(TEMPLATES['Timestamp'], {
            'created': created,
            'expires': expires,
        })
        digest_value = utils.digest(timestamp)
        signed_info = utils.prepare_template(TEMPLATES['SignedInfo'], {
            'uri': '#_0',
            'digest_value': digest_value,
        })
        signature_value = self.sign(signed_info)
        uuid = f'uuid-{uuid1()}-1'
        _logger.debug(f'''Creating Login Envelope with the next data
            "created": {created},
            "expires": {expires},
            "uuid": {uuid},
        ''')
        envelope = utils.prepare_template(TEMPLATES['LoginEnvelope'], {
            'binary_security_token': self.cert,
            'created': created,
            'digest_value': digest_value,
            'expires': expires,
            'signature_value': signature_value,
            'uuid': uuid,
        })
        return envelope

    def _get_login_data(self, response: str) -> str:
        '''Gets the token from the raw response'''
        response_dict = xmltodict.parse(response)
        self.token = response_dict['Envelope']['Body']['AutenticaResponse']['AutenticaResult']

    @ensure_login
    def query(self, start: datetime, end: datetime, download_type: str, request_type: str) -> str:
        '''Creates a Query in the SAT system'''
        request_content = self._get_query_soap_body(start, end, download_type, request_type)
        response = utils.consume(
            'http://DescargaMasivaTerceros.sat.gob.mx/ISolicitaDescargaService/SolicitaDescarga',
            'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc',
            request_content,
            token=self.token,
        )
        if response.status_code != 200:
            raise Exception(response.reason)
        else:
            try:
                id = self._get_query_id(utils.remove_namespaces(response.content.decode('UTF-8')))
                return id
            except:
                raise  # TODO

    def _get_query_soap_body(self, start: datetime, end: datetime, download_type: str, request_type: str):
        '''Creates the SOAP body to the query request'''
        start = start.isoformat()
        end = end.isoformat()
        data = {
            'start': start,
            'end': end,
            'rfc': self.rfc,
            'download_type': download_type,
            'request_type': request_type,
            'signature': '',
        }
        envelope = self._create_common_envelope(TEMPLATES['SolicitaDescarga'], data)
        return envelope

    def _get_query_id(self, response: str) -> str:
        '''Gets the Query ID from the raw response'''
        response_dict = xmltodict.parse(response)
        result = response_dict['Envelope']['Body']['SolicitaDescargaResponse']['SolicitaDescargaResult']
        status_code = int(result.get('@CodEstatus', -1))
        if status_code == 5000:
            id = result['@IdSolicitud']
            return id
        message = result['@Mensaje']
        raise Exception(f'Error in query ({status_code}): {message}')

    @ensure_login
    def verify(self, query_id: str) -> dict:
        '''Checks the status of a Query'''
        request_content = self._get_verify_soap_body(query_id)
        response = utils.consume(
            'http://DescargaMasivaTerceros.sat.gob.mx/IVerificaSolicitudDescargaService/VerificaSolicitudDescarga',
            'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/VerificaSolicitudDescargaService.svc',
            request_content,
            token=self.token,
        )
        if response.status_code != 200:
            raise Exception(response.reason)
        else:
            try:
                data = self._get_verify_data(utils.remove_namespaces(response.content.decode('UTF-8')))
                return data
            except:
                raise  # TODO

    def _get_verify_soap_body(self, query_id: str) -> str:
        '''Creates the SOAP body to check the query status'''
        data = {
            'rfc': self.rfc,
            'query_id': query_id,
            'signature': '',
        }
        envelope = self._create_common_envelope(TEMPLATES['VerificaSolicitudDescarga'], data)
        return envelope

    def _get_verify_data(self, response: str) -> dict:
        '''Gets the Query ID from the raw response'''
        response_dict = xmltodict.parse(response)
        result = response_dict['Envelope']['Body']['VerificaSolicitudDescargaResponse']['VerificaSolicitudDescargaResult']
        data = {
            'EstadoSolicitud': result['@EstadoSolicitud'],
            'CodEstatus': result['@CodEstatus'],
            'Mensaje': result['@Mensaje'],
            'CodigoEstadoSolicitud': result['@CodigoEstadoSolicitud'],
            'NumeroCFDIs': result['@NumeroCFDIs'],
            'IdsPaquetes': result['IdsPaquetes'] if result['@EstadoSolicitud'] == '3' else '',  # TODO Check what happens when multiple ids
        }
        return data

    @ensure_login
    def download(self, package_ids: (list, str)) -> dict:
        '''Checks the status of a Query'''
        if type(package_ids) == str:
            package_ids = [package_ids]
        downloads = {}
        for package_id in package_ids:
            request_content = self._get_download_soap_body(package_id)
            response = utils.consume(
                'http://DescargaMasivaTerceros.sat.gob.mx/IDescargaMasivaTercerosService/Descargar',
                'https://cfdidescargamasiva.clouda.sat.gob.mx/DescargaMasivaService.svc',
                request_content,
                token=self.token,
            )
            if response.status_code != 200:
                raise Exception(response.reason)
            else:
                try:
                    downloads[package_id] = self._get_download_data(utils.remove_namespaces(response.content.decode('UTF-8')))
                except:
                    raise  # TODO
        return downloads

    def _get_download_soap_body(self, package_id: str) -> dict:
        '''Creates the SOAP body to check the query status'''
        data = {
            'rfc': self.rfc,
            'package_id': package_id,
            'signature': '',
        }
        envelope = self._create_common_envelope(TEMPLATES['PeticionDescargaMasivaTercerosEntrada'], data)
        return envelope

    def _get_download_data(self, response: str) -> bytes:
        '''Gets the Download data from the raw response'''
        response_dict = xmltodict.parse(response)
        package = response_dict['Envelope']['Body']['RespuestaDescargaMasivaTercerosSalida']['Paquete']
        return package and base64.b64decode(package)

    def wait_query(self, query_id: str, retries: int = 10, wait_seconds: int = 2) -> list:
        for _ in range(retries):
            verification = self.verify(query_id)
            if verification['EstadoSolicitud'] == '3':
                return verification['IdsPaquetes']
            time.sleep(wait_seconds)
        else:
            raise TimeoutError('The query is not yet resolved')
