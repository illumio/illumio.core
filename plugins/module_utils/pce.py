#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2022 Illumio, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import sys
import traceback
from abc import ABCMeta, abstractmethod
from typing import Any

from ansible.module_utils.basic import AnsibleModule, missing_required_lib, env_fallback

try:
    from illumio import PolicyComputeEngine, IllumioApiException, IllumioEncoder
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


class PceObjectApi(PceApiBase, metaclass=ABCMeta):
    _api: PolicyComputeEngine._PCEObjectAPI

    def get_by_href(self, href: str) -> Any:
        try:
            return self._api.get_by_reference(href)
        except IllumioApiException as e:
            self._module.fail_json(msg="Failed to get PCE object with HREF %s: %s" % (href, e))

    def get_by_name(self, name: str) -> Any:
        try:
            objects = self._api.get(params={'name': name, 'max_results': 1})
            if not objects:
                return None
            return objects[0]
        except IllumioApiException as e:
            self._module.fail_json(msg="Failed to get PCE object with name %s: %s" % (name, e))

    def create(self, o: Any) -> Any:
        try:
            return self._api.create(o)
        except IllumioApiException as e:
            self._module.fail_json(msg="Failed to create PCE object: %s" % (e))

    def update(self, remote_object: Any, o: Any) -> bool:
        if not remote_object or not remote_object.href:
            self._module.fail_json(msg="Failed to update PCE object: invalid remote object")
        if self.params_match(remote_object):
            return False
        try:
            self._api.update(remote_object.href, o)
            return True
        except IllumioApiException as e:
            self._module.fail_json(msg="Failed to update PCE object: %s" % (e))

    def delete(self, o: Any) -> bool:
        if not o or not o.href:
            return False
        try:
            self._api.delete(o.href)
            return True
        except IllumioApiException as e:
            self._module.fail_json(msg="Failed to delete PCE object: %s" % (e))

    @abstractmethod
    def params_match(self, o: Any) -> bool:
        """Returns true if the parameters of the remote object match the Ansible
        module inputs.

        Used to determine whether an update is required.

        Args:
            o (Any): the decoded remote object
        """

    def json_output(self, o: Any) -> Any:
        return json.loads(json.dumps(o, cls=IllumioEncoder))


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
            type='str',
            default='443',
            fallback=(env_fallback, ['ILLUMIO_PCE_PORT'])
        ),
        pce_org_id=dict(
            type='str',
            default='1',
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
