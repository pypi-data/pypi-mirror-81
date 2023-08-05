import random
import string
import base64
import pytest
from .authing import Authing, SDKInitException
from .lib import (
    getTokenInfo,
    encodePasswd,
    createGqlClient,
    execQuery
)
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJQb29sSWQiOiI1ZTcyZDY1Yzc3OTMyYTU5YTI2NmE1Y2EiLCJhcHBJZCI6bnVsbCwidXNlcklkIjoiNWYwZTZmM2YwNmM1Yjc2YjdiOGE4NjVkIiwiYXJuIjoiYXJuOmNuOmF1dGhpbmc6NWU3MmQ2NWM3NzkzMmE1OWEyNjZhNWNhOnVzZXI6NWYwZTZmM2YwNmM1Yjc2YjdiOGE4NjVkIiwiaWQiOiI1ZjBlNmYzZjA2YzViNzZiN2I4YTg2NWQiLCJfaWQiOiI1ZjBlNmYzZjA2YzViNzZiN2I4YTg2NWQiLCJwaG9uZSI6IjE3NjExMTYxNTUwIiwiZW1haWwiOiJ0ZXN0QHRlc3QuY29tIiwidXNlcm5hbWUiOiJ0ZXN0IiwidW5pb25pZCI6bnVsbCwib3BlbmlkIjpudWxsfSwiaWF0IjoxNjAxMjg4MTkxLCJleHAiOjE2MDI1ODQxOTF9.pkjenEyqPDCb0s2l0XMNQ9UJGEZOfzieBH8yTPcvMLM'
PUBKEY = '''
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC4xKeUgQ+Aoz7TLfAfs9+paePb
5KIofVthEopwrXFkp8OCeocaTHt9ICjTT2QeJh6cZaDaArfZ873GPUn00eOIZ7Ae
+TiA2BKHbCvloW3w5Lnqm70iSsUi5Fmu9/2+68GZRH9L7Mlh8cFksCicW2Y2W2uM
GKl64GDcIq3au+aqJQIDAQAB
-----END PUBLIC KEY-----
'''
API_ENDPOINT = 'https://core.authing.cn/graphql'
TEST_USERNAME = 'test'
TEST_PASSWORD = '123456'
userPoolId = '5e72d65c77932a59a266a5ca'
secret = '699b99005bdf51d5f7ca97014ed9fdea'


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters).lower() for i in range(length))
    return result_str


def test_getTokenInfo():
    data = getTokenInfo(TOKEN)['data']

    assert data['email'] == "test@test.com"
    assert data['id'] == "5f0e6f3f06c5b76b7b8a865d"
    assert data['userPoolId'] == "5e72d65c77932a59a266a5ca"


def test_tokenExpCheck():
    pass


def test_encodePasswd():
    password = str(random.randint(10000, 99999))
    assert password


def test_createGqlClient():
    client = createGqlClient(API_ENDPOINT)
    assert client


def test_SDKInit():
    auth = Authing({
        "userPoolId": userPoolId,
        "secret": secret,
    })
    assert auth.token


def test_SDKInit_fail():
    with pytest.raises(BaseException):
        assert Authing({
            "userPoolId": userPoolId,
            "secret": '1111',
        })


def test_TokenRequest():
    auth = Authing({
        "userPoolId": userPoolId,
        "secret": secret,
    })
    res = auth.checkLoginStatus({
        "token": auth.token
    })
    assert res


def test_login():
    auth = Authing({"userPoolId": userPoolId, })
    auth.login({
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
    })
    assert auth.token


def test_register():
    username = get_random_string(10)
    password = get_random_string(10)
    auth = Authing({"userPoolId": userPoolId, "secret": secret})
    res = auth.register({
        "username": username,
        "password": password
    })
    assert res['username'] == username


def test_users():
    auth = Authing({
        "userPoolId": userPoolId,
        "secret": secret,
    })
    res = auth.users()
    assert res


def test_sendPhoneCode():
    auth = Authing({
        "userPoolId": userPoolId,
        "secret": secret,
    })
    res = auth.sendPhoneCode()
    assert res['code'] == 200


def test_resetPasswordByPhoneCode():
    auth = Authing({
        "userPoolId": userPoolId,
        "secret": secret,
    })
    res = auth.resetPasswordByPhoneCode("17611161550", "", "123456")
    assert res['code'] == 200
