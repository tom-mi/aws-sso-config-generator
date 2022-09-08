from typing import Optional

from aws_sso_config_generator.client import Account, AccountRole


class ConfigWriter:
    def __init__(self, sso_start_url: str, sso_region: str, region: str, output: Optional[str]):
        self.sso_start_url = sso_start_url
        self.sso_region = sso_region
        self.region = region
        self.output = output

    def write_profile(self, account: Account, role: AccountRole):
        config = f'[profile {account.account_name.replace(" ", "")}-{role.role_name}]\n'
        config += f'sso_start_url = {self.sso_start_url}\n'
        config += f'sso_region = {self.sso_region}\n'
        config += f'sso_account_id = {account.account_id}\n'
        config += f'sso_role_name = {role.role_name}\n'
        config += f'region = {self.region}\n'
        if self.output:
            config += f'output = {self.output}\n'
        print(config)
