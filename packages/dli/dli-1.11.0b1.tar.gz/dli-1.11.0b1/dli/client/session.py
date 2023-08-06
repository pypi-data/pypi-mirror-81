#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import os
import warnings
import requests
import logging

from dli.client import _setup_logging
from dli.client.dli_client import DliClient
from dli import __version__


logger = logging.getLogger(__name__)
DEPRECATED_AGE = 1


def _set_pypi_url(package_name):
    return f"https://pypi.python.org/pypi/{package_name}/json"


def version_check(package_name):
    url = _set_pypi_url(package_name)

    try:
        data = requests.get(url).json()
        versions = list(x for x in data["releases"].keys() if 'b' not in x)
        versions = sorted(versions)
        versions.reverse()

        offset = versions.index(__version__)

        if offset > DEPRECATED_AGE:
            warnings.warn("You are using an old version of the SDK, please upgrade "
                          "using `pip install dli --upgrade` "
                          "before the SDK no longer functions as expected",
                          PendingDeprecationWarning)

    except requests.exceptions.SSLError as e:
        # Version check has been see to fail by Gilberto with an SSLError
        # when doing the handshake with pypi.
        logger.warning(f'SSLError pypi version_check:',
                       extra={'SSLError': e})
    except Exception:
        pass


def _start_session(
    api_key=None,
    root_url="https://catalogue.datalake.ihsmarkit.com/__api",
    host=None,
    debug=False,
    strict=True,
    use_keyring=True,
    log_level=None,
):
    if log_level is None:
        log_level = 'stderr:info'
    logger = _setup_logging(log_level)

    #version_check('dli')

    user = os.environ.get("DLI_ACCESS_KEY_ID")
    pasw = os.environ.get("DLI_SECRET_ACCESS_KEY")
    api_key = api_key or os.environ.get("DLI_API_KEY")

    logger.debug("Checking auth flow")

    try:
        if (user is not None and pasw is not None) and api_key is None:
            logger.debug("Using SAM client credentials authentication flow")
            return get_client()(root_url, host, debug=debug, strict=strict,
                                access_id=user, secret_key=pasw, use_keyring=use_keyring)
        elif (user is None or pasw is None) and api_key is None:
            logger.debug("Using SAM PKCE web authentication flow")
            return get_client()(root_url, host, debug=debug, strict=strict, use_keyring=use_keyring)
        elif api_key is not None:
            logger.debug("Using API Key authentication flow")
            if api_key is not None:
                return get_client()(root_url, host, debug=debug, strict=strict,
                                    secret_key=api_key, use_keyring=use_keyring)
    except SystemExit:
        return


def start_session(*args, **kwargs):
    """
    .. deprecated:: 1.8.3


    Entry point for the Data Lake SDK, returns a client instance that
    can be used to consume or register datasets.

    Example for creating a client:

        from dli.client import session
        client = session.start_session()

    :param str api_key: Your API key, can be retrieved from your dashboard in
                        the Catalogue UI.
    :param str root_url: Optional. The environment you want to point to. By default it
                        points to Production.
    :param str host: Optional. Advanced usage, meant to force a hostname when DNS resolution
                     is not reacheable from the user's network.
                     This is meant to be used in conjunction with an
                     IP address as the root url.
                     Example: catalogue.datalake.ihsmarkit.com

    :param bool debug: Optional. Log SDK operations to a file in the current working
                       directory with the format "sdk-{end of api key}-{timestamp}.log"

    :param bool strict: Optional. When True, all exception messages and stack
                        trace are printed. When False, a shorter message is
                        printed and `None` should be returned.
    :param bool use_keyring: Optional. When True, cache the JWT in the system keyring
                             and retrieve that JWT from the system keyring if set.
                             Otherwise disable the keyring completely.

    :returns: Data Lake interface client
    :rtype: dli.client.dli_client.DliClient

    .. deprecated:: 1.8.3

        `api_key`: please use the basic flow or client credentials.

    """
    warnings.warn(
        'start_session is deprecated. To create a client: \n\n'
        '\t\timport dli\n'
        '\t\tdli.connect()\n',
        DeprecationWarning
    )

    return _start_session(*args, **kwargs)


def get_client():
    return DliClient
