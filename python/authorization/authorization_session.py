import logging
import traceback

from datetime import datetime, timedelta
from os import environ

from requests import adapters, Session
from requests.auth import HTTPBasicAuth
from urllib3.util import Retry

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

USER_AGENT = "backend/2021-02-02"
logger = logging.getLogger(__name__)

class BackendSession(object):
    def __init__(self):
        self.has_client = False
        self.vault_client = self.get_vault_client()
        self.session_open = False
        self.session = self.get_session()
        self.expires_at = datetime.utcnow()
        self.token = self.__get_token__()


        def get_vault_client(self):
            "vault access"

        def __get_client_secret__(self):
            if ENVIRONMENT == c.ENV_LOCAL:
                logger.info(
                    "Running locally, getting client secret from environment variable"
                )
                return environ.get("CLIENT_SECRET", None)
            try:
                secret = self.vault_client.GET_SECRET()
                LOGGER.INFO("Successfully obtained Client Secret")
            except Exception as e:
                logger.exception(f"Failed to get secret for secret key {CLENT_SECRET_KEY}; error={e}")
                logger.error(f"Uncaught exception: {traceback.format_exc()})
                return "No Secret"
            return secret

        def __get_token__(self):
            if self.session is None:
                return None
            elif self.expires_at > datetime.utcnow():
                return self.token
            else:
                logger.info("OAuth2 token has expired, requesting new token")
                auth = HTTPBasicAuth(CLIENT_ID, self.__get_client_secret__())
                try:
                    response = self.session.post(
                        OAUTH2_URL,
                        params = {"grant_type": "client_credentials"},
                        verify=SSL_VERIFY,
                        auth=auth,
                        timeout=60,
                        headers={
                            "user-agent": USER_AGENT,
                            "cache-control": "no-cache",
                            "content-type": "application/x-www-form-urlencoded",
                        },
                    )
                except:
                    logger.exception(
                        f"Oauth2 request failed for client: {CLIENT_ID}, url: {OAUTH2_URL}"
                    )
                    logger.error(f"Uncaught exception: {traceback.format_exc()}")
                if response.status_code != 200:
                    err_msg = f"oauth2 request to +>{OAUTH2_URL} FAILED WITH STATUS CODE =>{response.status_code}"
                    logger.warning(err_msg)
                    return "No token"

                token_data = response.json()
                access_token = token_data["access_token"]
                issued_at = datetime.utcfromtimestamp(token_data["issued_at"])
                self.expires_at = issued_at + timedelta(0, (token_data["expires_in"] - 1800))
                return access_token

            def get_session(self):
                if self.session_open:
                    return self.session
                else:
                    logger.info("Authorization session has closed, crreating a new session")
                    session = Session()
                    try:
                        retries = Retry(
                            total=4,
                            read=4,
                            connect=4,
                            backoff_factor=1.5,
                            status_forcelist=(404, 500, 502, 503, 504),
                            method_whitelist=(["GET", "POST", "PUT"])
                        )
                        session.mount(
                            "http://",
                            adapters.HTTPAdapter(
                                pool_connections=MAX_WORKERS,
                                pool_maxsize=MAX_WORKERS,
                                max_retries=retries,
                            )
                            logger.info("Successfully created authorization session")
                            self.session_open = True
                        )
                        return session
                    except:
                        logger.exception("Failed to create authorization session")
                        logger.error(f"Uncaught exception: {traceback.format_exc()}")
                        return None

            def get_authorization_headers(self):
                return {
                    "Authorization": f"Bearer {self.__get_token__()}",
                    "Accept": f"application/json;v={APP_VERSION}",
                    "Content-Type": "application/json",
                    "Cache-Control": "no-cache",
                    "user-agent": USER_AGENT,
                }
