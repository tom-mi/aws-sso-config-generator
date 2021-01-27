import sys
import time
from dataclasses import dataclass
from typing import List

import boto3
import webbrowser


@dataclass
class Account:
    account_id: str
    account_name: str


@dataclass
class AccountRole:
    account_id: str
    role_name: str


class AwsSsoClient:
    def __init__(self, region: str, start_url: str):
        self.sso_oidc_client = boto3.client('sso-oidc', region_name=region)
        self.sso_client = boto3.client('sso', region_name=region)

        self._register_client()
        self._start_device_authorization(start_url)
        webbrowser.open(self.verification_uri_complete)
        self._get_access_token()

    def _register_client(self):
        response = self.sso_oidc_client.register_client(
            clientName='aws-sso-config-generator',
            clientType='public',
        )
        self.client_id = response['clientId']
        self.client_secret = response['clientSecret']

    def _start_device_authorization(self, start_url: str):
        response = self.sso_oidc_client.start_device_authorization(
            clientId=self.client_id,
            clientSecret=self.client_secret,
            startUrl=start_url,
        )
        self.device_code = response['deviceCode']
        self.user_code = response['userCode']
        self.verification_uri_complete = response['verificationUriComplete']
        self.interval = response['interval']

    def _get_access_token(self):
        sys.stderr.write('Attempting to open the AWS SSO authorization page in your default browser. Please confirm '
                         'login ...\n')
        while True:
            try:
                response = self.sso_oidc_client.create_token(
                    clientId=self.client_id,
                    clientSecret=self.client_secret,
                    grantType='urn:ietf:params:oauth:grant-type:device_code',
                    deviceCode=self.device_code,
                )
            except self.sso_oidc_client.exceptions.AuthorizationPendingException:
                time.sleep(self.interval)
                continue
            self.access_token = response['accessToken']
            return

    def list_accounts(self) -> List[Account]:
        response = []
        paginator = self.sso_client.get_paginator('list_accounts')
        for page in paginator.paginate(accessToken=self.access_token):
            for item in page['accountList']:
                response.append(Account(account_id=item['accountId'], account_name=item['accountName']))
        return response

    def list_account_roles(self, account_id: str) -> List[AccountRole]:
        response = []
        paginator = self.sso_client.get_paginator('list_account_roles')
        for page in paginator.paginate(accessToken=self.access_token, accountId=account_id):
            for item in page['roleList']:
                response.append(AccountRole(account_id=item['accountId'], role_name=item['roleName']))
        return response
