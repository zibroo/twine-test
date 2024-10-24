import os
import boto3
import hvac
from aws_lambda_powertools import Logger

logger = Logger()

class VaultAuth:
    def __init__(self, vault_addr=None, vault_role=None):
        self.vault_addr = vault_addr or os.getenv('VAULT_ADDR')
        self.vault_role = vault_role or os.getenv('VAULT_ROLE')
        self.client = hvac.Client(url=self.vault_addr)

    def authenticate(self):
        try:
            # Initialize AWS session and get credentials
            session = boto3.Session()
            credentials = session.get_credentials().get_frozen_credentials()

            # Authenticate with Vault using AWS IAM
            self.client.auth.aws.iam_login(
                access_key=credentials.access_key,
                secret_key=credentials.secret_key,
                session_token=credentials.token,
                role=self.vault_role,
            )
            if self.client.is_authenticated():
                logger.info("Vault authentication successful.")
                return True
            else:
                logger.error("Failed to authenticate to Vault.")
                return False
        except Exception as e:
            logger.error(f"Error during Vault authentication: {e}")
            return False

    def get_secret(self, secret_path, secret_keys):
        if not self.client.is_authenticated():
            logger.error("Vault client is not authenticated.")
            return None

        try:
            # Retrieve the secret from the specified path
            secret_response = self.client.secrets.kv.v1.read_secret(path=secret_path)
            secret_data = secret_response.get('data', {})
            logger.info(f"Retrieved secret from '{secret_path}'.")

            # Extract only the requested keys
            return {key: secret_data.get(key) for key in secret_keys}
        except Exception as e:
            logger.error(f"Error retrieving secret from Vault: {e}")
            return None
