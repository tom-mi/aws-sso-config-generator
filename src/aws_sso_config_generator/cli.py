import argparse
import os

from aws_sso_config_generator.client import AwsSsoClient
from aws_sso_config_generator.config import ConfigWriter


def main():
    config = _parse_config()

    client = AwsSsoClient(region=config.region, start_url=config.start_url)
    writer = ConfigWriter(sso_start_url=config.start_url, sso_region=config.sso_region, region=config.region,
                          output=config.output)

    accounts = client.list_accounts()
    for account in sorted(accounts, key=lambda a: a.account_name):
        roles = client.list_account_roles(account.account_id)
        for role in sorted(roles, key=lambda r: r.role_name):
            writer.write_profile(account, role)


def _parse_config():
    parser = argparse.ArgumentParser(description='Generate AWS SSO named profiles for ~/.aws/config')
    parser.add_argument('--region', metavar='REGION', required=True, help='AWS region for generated profiles')
    parser.add_argument('--sso-region', metavar='REGION', required=True, help='AWS SSO region')
    parser.add_argument('--start-url', metavar='URL', required=True, help='AWS SSO start url')
    parser.add_argument('--output', help='output format for generated profiles')
    args = parser.parse_args()

    return args
