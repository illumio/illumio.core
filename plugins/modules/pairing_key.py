#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2022 Illumio, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: pairing_key
short_description: Generate pairing key from an Illumio PCE pairing profile
description: This module allows you to generate pairing keys on the Illumio PCE that can be used to pair Illumio VEN agents
author:
  - Duncan Sommerville (@dsommerville-illumio)
requirements:
  - "python>=3.6"
  - "illumio>=1.0.0"
version_added: "0.2.0"

options:
    pairing_profile_name:
        description: Name of an existing pairing profile.
        type: str
    pairing_profile_href:
        description: HREF of an existing pairing profile.
        type: str

extends_documentation_fragment:
  - illumio.illumio.pce
'''

EXAMPLES = r'''
- name: "Generate pairing key by profile name"
  illumio.illumio.pairing_key:
    pairing_profile_name: Default
  register: pairing_key_result

- name: "Generate pairing key by profile HREF"
  illumio.illumio.pairing_key:
    pairing_profile_href: /orgs/1/pairing_profiles/1
  register: pairing_key_result
'''

RETURN = r'''
pairing_key:
    description: The generated pairing key.
    type: str
    returned: success
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.illumio.illumio.plugins.module_utils.pce import PceApiBase, pce_connection_spec  # type: ignore

from illumio.exceptions import IllumioApiException


class PairingKeyApi(PceApiBase):
    def get_by_profile_href(self, profile_href):
        try:
            return self._pce.generate_pairing_key(profile_href)
        except IllumioApiException as e:
            self._module.fail_json("Failed to generate pairing key for profile with HREF '%s': %s" % (profile_href, e))

    def get_by_profile_name(self, profile_name):
        try:
            profiles = self._pce.pairing_profiles.get(params={'name': profile_name, 'max_results': 1})
            if not profiles:
                self._module.fail_json("No pairing profile found with name '%s'" % profile_name)
            return self.get_by_profile_href(profiles[0].href)
        except IllumioApiException as e:
            self._module.fail_json(msg="Failed to get pairing profile with name '%s': %s" % (profile_name, e))


def spec():
    return dict(
        pairing_profile_name=dict(type='str'),
        pairing_profile_href=dict(type='str')
    )


def main():
    argument_spec = pce_connection_spec()
    argument_spec.update(spec())

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[['pairing_profile_name', 'pairing_profile_href']],
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(changed=False, pairing_key='')

    pairing_key_api = PairingKeyApi(module)

    profile_name = module.params.get('pairing_profile_name')
    profile_href = module.params.get('pairing_profile_href')

    if profile_href:
        pairing_key = pairing_key_api.get_by_profile_href(profile_href)
    elif profile_name:
        pairing_key = pairing_key_api.get_by_profile_name(profile_name)
    else:
        module.fail_json("A valid value for one of pairing_profile_name or pairing_profile_href must be provided")

    module.exit_json(changed=True, pairing_key=pairing_key)


if __name__ == '__main__':
    main()
