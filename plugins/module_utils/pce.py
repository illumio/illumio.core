#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2022 Illumio, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys
import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib, env_fallback

try:
    from illumio import PolicyComputeEngine
except ImportError:
    PolicyComputeEngine = None
    # replicate the traceback formatting from AnsibleModule.fail_json
    IMPORT_ERROR_TRACEBACK = ''.join(traceback.format_tb(sys.exc_info()[2]))


class PceApiBase(object):
    """Base class for modules interacting with the PCE API."""
    def __init__(self, module: AnsibleModule):
        self._module = module

        if not PolicyComputeEngine:
            module.fail_json(
                msg=missing_required_lib('illumio', url='https://pypi.org/project/illumio/'),
                exception=IMPORT_ERROR_TRACEBACK
            )

        hostname = module.params.get('pce_hostname')
        port = module.params.get('pce_port')
        org_id = module.params.get('pce_org_id')
        api_key_username = module.params.get('api_key_username')
        api_key_secret = module.params.get('api_key_secret')

        self._pce = PolicyComputeEngine(hostname, port=port, org_id=org_id)
        self._pce.set_credentials(api_key_username, api_key_secret)

        if not self._pce.check_connection():
            module.fail_json("Failed to establish a connection to the PCE.")


def pce_connection_spec() -> dict:
    """Modules interacting with the PCE APIs extend this specification."""
    return dict(
        pce_hostname=dict(
            type='str',
            required=True,
            aliases=['pce_url'],
            fallback=(env_fallback, ['ILLUMIO_PCE_HOST'])
        ),
        pce_port=dict(
            type='int',
            default=443,
            fallback=(env_fallback, ['ILLUMIO_PCE_PORT'])
        ),
        pce_org_id=dict(
            type='int',
            default=1,
            fallback=(env_fallback, ['ILLUMIO_PCE_ORG_ID'])
        ),
        api_key_username=dict(
            type='str',
            required=True,
            no_log=True,
            fallback=(env_fallback, ['ILLUMIO_API_KEY_USERNAME'])
        ),
        api_key_secret=dict(
            type='str',
            required=True,
            no_log=True,
            fallback=(env_fallback, ['ILLUMIO_API_KEY_SECRET'])
        )
    )
