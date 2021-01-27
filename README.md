# aws-sso-config-generator

Generate AWS SSO named profiles for `~/.aws/config`

## Installation

```
pip install git+https://github.com/tom-mi/aws-sso-config-generator#subdirectory=src
```

## Usage

```
generate-aws-sso-config --start-url https://example.awsapps.com/start --output json --region eu-west-1 --sso-region eu-west-1
```

This command opens the AWS SSO login page in a browser. After successful login, the command iterates over all AWS
accounts & roles available via the given AWS SSO login and prints out configuration snippets suitable for
`~/.aws/config`, e.g.
```
[profile some-account-developer]
sso_start_url = https://example.awsapps.com/start
sso_region = eu-west-1
sso_account_id = 123456789012
sso_role_name = developer
region = eu-west-1
output = json
```

The profile names are `${account_name}-${role_name}`.
