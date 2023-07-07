# flake8: noqa
"""Source: https://github.com/SumSubstance/AppTokenUsageExamples/blob/master/Python/AppTokenPythonExample.py"""
import hashlib
import hmac
import json
import logging
import time
import uuid
import os
from typing import Optional

import requests

SUMSUB_TEST_BASE_URL = "https://api.sumsub.com"
REQUEST_TIMEOUT = 60
# Please don't forget to change token and secret key values to production ones when switching to production

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)

def generate_sumsub_token(uid: str, level_name: str, ttl_in_secs: Optional[int]=600) -> str:
    """Generates a Sumsub access token.

    Args:
        uid (str): The external user ID which will be bound to the token.
        level_name (str): The name of the level configured in the dashboard.
        ttl_in_secs (int, optional): Lifespan of a token in seconds. Default is 600 seconds.

    Returns:
        str: A newly generated access token for an applicant.
    """
    url = SUMSUB_TEST_BASE_URL + f'/resources/accessTokens?userId={uid}&levelName={level_name}'
    if ttl_in_secs is not None:
        url += f'&ttlInSecs={ttl_in_secs}'
    resp = sign_request(requests.Request('POST', url))
    s = requests.Session()
    response = s.send(resp, timeout=REQUEST_TIMEOUT)
    LOG.debug(f"Sumsub generate_sumsub_token response: {response.json()}")
    return response.json().get('token')

def create_applicant(external_user_id, level_name):
    # https://developers.sumsub.com/api-reference/#creating-an-applicant
    body = {'externalUserId': external_user_id}
    params = {'levelName': level_name}
    headers = {
        'Content-Type': 'application/json',
        'Content-Encoding': 'utf-8'
    }
    resp = sign_request(
        requests.Request('POST', SUMSUB_TEST_BASE_URL + '/resources/applicants?levelName=' + level_name,
                         params=params,
                         data=json.dumps(body),
                         headers=headers))
    s = requests.Session()
    response = s.send(resp, timeout=REQUEST_TIMEOUT)
    LOG.debug(f"Sumsub create_applicant response: {response.json()}")
    applicant_id = (response.json()['id'])
    return applicant_id


def add_document(applicant_id):
    # https://developers.sumsub.com/api-reference/#adding-an-id-document
    with open('img.jpg', 'wb') as handle:
        response = requests.get('https://fv2-1.failiem.lv/thumb_show.php?i=gdmn9sqy&view', stream=True,
                                timeout=REQUEST_TIMEOUT)
        if not response.ok:
            logging.error(response)

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    payload = {"metadata": '{"idDocType":"PASSPORT", "country":"USA"}'}
    resp = sign_request(
        requests.Request('POST', SUMSUB_TEST_BASE_URL + '/resources/applicants/' + applicant_id + '/info/idDoc',
                         data=payload,
                         files=[('content', open('img.jpg', 'rb'))]
                         ))
    sw = requests.Session()
    response = sw.send(resp, timeout=REQUEST_TIMEOUT)
    LOG.debug(f"Sumsub add_document response: {response.json()}")
    return response.headers['X-Image-Id']


def get_applicant_status(applicant_id):
    # https://developers.sumsub.com/api-reference/#getting-applicant-status-api
    url = SUMSUB_TEST_BASE_URL + '/resources/applicants/' + applicant_id + '/status'
    resp = sign_request(requests.Request('GET', url))
    s = requests.Session()
    response = s.send(resp, timeout=REQUEST_TIMEOUT)
    LOG.debug(f"Sumsub get_applicant_status response: {response.json()}")
    return response.json()


def get_access_token(external_user_id, level_name):
    # https://developers.sumsub.com/api-reference/#access-tokens-for-sdks
    params = {'userId': external_user_id, 'ttlInSecs': '600', 'levelName': level_name}
    headers = {'Content-Type': 'application/json',
               'Content-Encoding': 'utf-8'
               }
    resp = sign_request(requests.Request('POST', SUMSUB_TEST_BASE_URL + '/resources/accessTokens',
                                         params=params,
                                         headers=headers))
    s = requests.Session()
    response = s.send(resp, timeout=REQUEST_TIMEOUT)
    LOG.debug(f"Sumsub get_access_token response: {response.json()}")
    token = (response.json()['token'])

    return token

def sign_request(request: requests.Request) -> requests.PreparedRequest:
    prepared_request = request.prepare()
    now = int(time.time())
    method = request.method.upper()
    path_url = prepared_request.path_url  # includes encoded query params
    # could be None so we use an empty **byte** string here
    body = b'' if prepared_request.body is None else prepared_request.body
    if type(body) == str:
        body = body.encode('utf-8')
    data_to_sign = str(now).encode('utf-8') + method.encode('utf-8') + path_url.encode('utf-8') + body
    # hmac needs bytes
    signature = hmac.new(
        os.environ['SUMSUB_SECRET_KEY'].encode('utf-8'),
        data_to_sign,
        digestmod=hashlib.sha256
    )
    prepared_request.headers['X-App-Token'] = os.environ['SUMSUB_APP_TOKEN']
    prepared_request.headers['X-App-Access-Ts'] = str(now)
    prepared_request.headers['X-App-Access-Sig'] = signature.hexdigest()
    return prepared_request


# # Such actions are presented below:
# # 1) Creating an applicant
# # 2) Adding a document to the applicant
# # 3) Getting applicant status
# # 4) Getting access token
# def sumsub():
#     logging.basicConfig(level=logging.INFO)
#     external_user_id = str(uuid.uuid4())
#     level_name = 'basic-kyc-level'
#     applicant_id = create_applicant(external_user_id, level_name)
#     logging.info(applicant_id)
#     image_id = add_document(applicant_id)
#     logging.info(image_id)
#     status = get_applicant_status(applicant_id)
#     logging.info(status)
#     token = get_access_token(external_user_id, level_name)
#     logging.info(token)
