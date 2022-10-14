#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2022 Illumio, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: pairing_profile
short_description: Create/update/delete Illumio PCE pairing profiles
description:
  - This module allows you to create and manipulate pairing profile objects on the Illumio PCE to pair Illumio VEN agents.
  - Supports check mode.

author:
  - Duncan Sommerville (@dsommerville-illumio)
requirements:
  - "python>=3.6"
  - "illumio>=1.1.1"
version_added: "0.2.0"

options:
  href:
    description: HREF of an existing pairing profile.
    type: str
  name:
    description:
      - Pairing profile display name.
      - Required for creating a pairing profile or when HREF is not specified.
    type: str
  description:
    description: Pairing profile description.
    type: str
  state:
    description:
      - Desired pairing profile state.
      - If C(present), the profile will be created if it does not exist, or updated to match the provided parameters if it does.
      - If C(absent), the profile will be removed if it exists.
    type: str
    choices: ['present', 'absent']
    default: 'present'
  enabled:
    description: Determines whether or not the profile is enabled for pairing.
    type: bool
    default: 'yes'
  enforcement_mode:
    description:
      - Pairing profile default enforcement mode.
      - VENs paired using this profile will be put into the provided enforcement mode by default.
      - "C(idle): the VEN will not take control of the host firewall."
      - "C(visibility_only): no traffic will be blocked by PCE policy."
      - "C(selective): segmentation rules are enforced only for selected inbound services when the host is within the scope of an enforcement boundary."
      - "C(full): segmentation rules are enforced for all inbound and outbound services. Traffic that is not allowed by a segmentation rule is blocked."
    type: str
    choices: ['idle', 'visibility_only', 'selective', 'full']
    default: 'idle'
  enforcement_mode_lock:
    description: If set to C(false), allows the enforcement mode to be overridden when pairing.
    type: bool
    default: 'yes'
  visibility_level:
    description:
      - Determines what traffic will be logged by VENs paired with this profile.
      - "C(flow_summary): log connection information for allowed, blocked, and potentially blocked traffic."
      - "C(flow_drops): log connection information for blocked and potentially blocked traffic."
      - "C(flow_off): do not log any traffic information."
      - "C(enhanced_data_collection): log byte counts in addition to connection details for all traffic."
    type: str
    choices: ['flow_summary', 'flow_drops', 'flow_off', 'enhanced_data_collection']
    default: 'flow_summary'
  visibility_level_lock:
    description: If set to C(false), allows the visibility level to be overridden when pairing.
    type: bool
    default: 'yes'
  allowed_uses_per_key:
    description:
      - The number of times pairing profile keys can be used.
      - By default, each key has unlimited uses.
    type: str
    default: 'unlimited'
  key_lifespan:
    description:
      - The number of seconds pairing profile keys will be valid for.
      - By default, each key lasts an unlimited amount of time.
    type: str
    default: 'unlimited'
  ven_version:
    description:
      - Optional parameter to set the VEN version used by this pairing profile.
      - If not set, the profile will use the default VEN version configured in the PCE's VEN library.
    type: str
  labels:
    description:
      - List of default labels to apply to workloads paired using this profile.
      - Labels can only be referenced by HREF, and only one Label of each type can be specified.
    type: list
    elements: dict
    default: []
    suboptions:
      href:
        description: Label HREF.
        type: str
        required: true
  role_label_lock:
    description: If set to C(false), allows the role label to be overridden when pairing.
    type: bool
    default: 'yes'
  app_label_lock:
    description: If set to C(false), allows the app label to be overridden when pairing.
    type: bool
    default: 'yes'
  env_label_lock:
    description: If set to C(false), allows the environment label to be overridden when pairing.
    type: bool
    default: 'yes'
  loc_label_lock:
    description: If set to C(false), allows the location label to be overridden when pairing.
    type: bool
    default: 'yes'
  external_data_set:
    description:
      - External data set identifier.
      - Must be set if using C(external_data_reference).
    type: str
  external_data_reference:
    description:
      - External data reference identifier.
      - Must be set if using C(external_data_set).
    type: str

extends_documentation_fragment:
  - illumio.core.pce
'''

EXAMPLES = r'''
- name: "Create profile with default labels"
  illumio.core.pairing_profile:
    name: PP-DB
    state: present
    enabled: yes
    labels:
      - href: /orgs/1/labels/1
      - href: /orgs/1/labels/2

- name: "Create profile with pairing key uses and lifespan limitations"
  illumio.core.pairing_profile:
    name: PP-AUTOMATION
    state: present
    enforcement_mode: visibility_only
    allowed_uses_per_key: 1
    key_lifespan: 30

- name: "Remove existing profile"
  illumio.core.pairing_profile:
    name: PP-DB
    state: absent

- name: "Remove profile by HREF"
  illumio.core.pairing_profile:
    href: /orgs/1/pairing_profiles/1
    state: absent
'''

RETURN = r'''
pairing_profile:
  description: Information about the pairing profile that was created or updated.
  type: complex
  returned: success
  contains:
    href:
      description: The pairing profile's HREF.
      type: str
      returned: always
    name:
      description: The pairing profile's name.
      type: str
      returned: always
    description:
      description: A description of the pairing profile.
      type: str
      returned: always
    enabled:
      description: A flag that determines whether or not this profile is enabled for pairing.
      type: bool
      returned: always
    enforcement_mode:
      description: The enforcement mode that will be applied to VENs paired using this profile.
      type: str
      returned: always
    enforcement_mode_lock:
      description: A flag that denotes whether the enforcement mode set by this profile can be overridden from the pairing script.
      type: bool
      returned: always
    visibility_level:
      description: Determines what traffic will be logged by VENs paired with this profile.
      type: str
      returned: always
    visibility_level_lock:
      description: A flag that denotes whether the visibility level set by this profile can be overridden from the pairing script.
      type: bool
      returned: always
    labels:
      description: A list of labels that will be applied to VENs paired using this profile.
      type: list
      returned: always
      elements: dict
      sample:
        - href: /orgs/1/labels/1
    role_label_lock:
      description: A flag that denotes whether the role label set by this profile can be overridden from the pairing script.
      type: bool
      returned: always
    app_label_lock:
      description: A flag that denotes whether the app label set by this profile can be overridden from the pairing script.
      type: bool
      returned: always
    env_label_lock:
      description: A flag that denotes whether the environment label set by this profile can be overridden from the pairing script.
      type: bool
      returned: always
    loc_label_lock:
      description: A flag that denotes whether the location label set by this profile can be overridden from the pairing script.
      type: bool
      returned: always
    allowed_uses_per_key:
      description: The number of times each pairing key generated by this profile can be used to pair VENs.
      type: str
      returned: always
    key_lifespan:
      description: The amount of time, in seconds, that a pairing key generated by this profile will be valid for.
      type: str
      returned: always
    agent_software_release:
      description: The VEN version used by this pairing profile.
      type: str
      returned: always
    is_default:
      description: A flag that denotes whether this profile is the default pairing profile for the PCE.
      type: bool
      returned: always
    total_use_count:
      description: The total number of times this profile has been used to pair VENs.
      type: int
      returned: always
    created_at:
      description: A timestamp denoting when this pairing profile was created.
      type: str
      returned: always
    created_by:
      description: A reference to the user object that created this profile.
      type: dict
      returned: always
      sample:
        created_by:
          href: /users/1
    updated_at:
      description: A timestamp denoting when this pairing profile was last updated.
      type: str
      returned: always
    updated_by:
      description: A reference to the user object that last updated this profile.
      type: dict
      returned: always
      sample:
        updated_by:
          href: /users/1
    caps:
      description:
        - Array of permissions on the entity held by the requesting user.
        - An empty array implies readonly permission.
      type: list
      elements: str
      returned: always

  sample:
    pairing_profile:
      href: /orgs/1/pairing_profiles/1500
      name: PP-ANSIBLE-TEST
      description: Created with Ansible
      enabled: true
      enforcement_mode: visibility_only
      enforcement_mode_lock: true
      visibility_level: flow_summary
      visibility_level_lock: true
      labels: []
      role_label_lock: true
      app_label_lock: true
      env_label_lock: true
      loc_label_lock: true
      allowed_uses_per_key: unlimited
      key_lifespan: unlimited
      agent_software_release: Default (21.2.0-7831)
      is_default: false
      total_use_count: 0
      created_at: "2022-06-07T00:11:10.923Z"
      created_by:
        href: /users/1
      updated_at: "2022-06-07T17:51:56.606Z"
      updated_by:
        href: /users/1
      caps:
        - write
        - generate_pairing_key
'''

import re
import sys
import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.illumio.core.plugins.module_utils.pce import PceObjectApi, pce_connection_spec  # type: ignore

try:
    from illumio.workloads import PairingProfile
except ImportError:
    PairingProfile = None
    # replicate the traceback formatting from AnsibleModule.fail_json
    IMPORT_ERROR_TRACEBACK = ''.join(traceback.format_tb(sys.exc_info()[2]))


class PairingProfileApi(PceObjectApi):
    def __init__(self, module: AnsibleModule) -> None:
        super().__init__(module)
        self._api = self._pce.pairing_profiles

    def params_match(self, o):
        ignore_params = ['href', 'state', 'labels', 'ven_version']
        params = [k for k in spec().keys() if k not in ignore_params]
        for k in params:
            if self._module.params.get(k) != getattr(o, k, None):
                return False
        return self._compare_labels(o) and self._compare_ven_version(o)

    def _compare_labels(self, profile):
        remote_labels = [label.href for label in getattr(profile, 'labels', [])]
        new_labels = [label['href'] for label in self._module.params.get('labels')]
        return remote_labels == new_labels

    def _compare_ven_version(self, profile):
        new_ven_version = self._module.params.get('ven_version')
        if not new_ven_version:  # if no version is specified in the module, skip
            return True
        remote_ven_version = getattr(profile, 'agent_software_release', '')
        match = re.match('^(?:Default \\()?([a-zA-Z0-9\\.-]+)\\)?$', remote_ven_version)
        # if a version is specified in the module, check if it matches the remote
        if match and match.group(1) != new_ven_version:
            return False
        return True


def spec():
    return dict(
        href=dict(type='str'),
        name=dict(type='str'),
        # if no description is provided when creating a profile, the PCE will
        # set the description to an empty string rather than a null value.
        # defaulting to an empty string ensures that comparisons behave as
        # expected when determining whether an update is needed.
        description=dict(type='str', default=''),
        state=dict(
            type='str',
            choices=['present', 'absent'],
            default='present'
        ),
        enabled=dict(type='bool', default=True),
        enforcement_mode=dict(
            type='str',
            choices=['idle', 'visibility_only', 'selective', 'full'],
            default='idle'
        ),
        enforcement_mode_lock=dict(type='bool', default=True),
        visibility_level=dict(
            type='str',
            choices=['flow_summary', 'flow_drops', 'flow_off', 'enhanced_data_collection'],
            default='flow_summary'
        ),
        visibility_level_lock=dict(type='bool', default=True),
        allowed_uses_per_key=dict(type='str', default='unlimited', no_log=False),
        key_lifespan=dict(type='str', default='unlimited', no_log=False),
        ven_version=dict(type='str'),
        labels=dict(
            type='list',
            default=[],
            elements='dict',
            options=dict(
                href=dict(
                    type='str',
                    required=True
                )
            )
        ),
        role_label_lock=dict(type='bool', default=True),
        app_label_lock=dict(type='bool', default=True),
        env_label_lock=dict(type='bool', default=True),
        loc_label_lock=dict(type='bool', default=True),
        external_data_set=dict(type='str'),
        external_data_reference=dict(type='str')
    )


def main():
    argument_spec = pce_connection_spec()
    argument_spec.update(spec())

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[['name', 'href']],
        required_together=[['external_data_set', 'external_data_reference']],
        supports_check_mode=True
    )

    if not PairingProfile:
        module.fail_json(
            msg=missing_required_lib('illumio', url='https://pypi.org/project/illumio/'),
            exception=IMPORT_ERROR_TRACEBACK
        )

    pairing_profile_api = PairingProfileApi(module)

    href = module.params.get('href')
    name = module.params.get('name')
    description = module.params.get('description')
    enabled = module.params.get('enabled')
    state = module.params.get('state')
    enforcement_mode = module.params.get('enforcement_mode')
    enforcement_mode_lock = module.params.get('enforcement_mode_lock')
    allowed_uses_per_key = module.params.get('allowed_uses_per_key')
    key_lifespan = module.params.get('key_lifespan')
    labels = module.params.get('labels')
    role_label_lock = module.params.get('role_label_lock')
    app_label_lock = module.params.get('app_label_lock')
    env_label_lock = module.params.get('env_label_lock')
    loc_label_lock = module.params.get('loc_label_lock')
    visibility_level = module.params.get('visibility_level')
    visibility_level_lock = module.params.get('visibility_level_lock')
    ven_version = module.params.get('ven_version')
    external_data_set = module.params.get('external_data_set')
    external_data_reference = module.params.get('external_data_reference')

    # the allowed_uses_per_key and key_lifespan fields default to 'unlimited'
    # but otherwise must be passed as integers. convert any numeric values
    # passed to integers
    allowed_uses_per_key = int(allowed_uses_per_key) if allowed_uses_per_key.isnumeric() else allowed_uses_per_key
    key_lifespan = int(key_lifespan) if key_lifespan.isnumeric() else key_lifespan

    if href:
        existing_profile = pairing_profile_api.get_by_href(href)
        if not existing_profile:
            module.fail_json("No pairing profile found with HREF %s" % (href))
    elif name:
        existing_profile = pairing_profile_api.get_by_name(name)

    if state == 'present':
        new_profile = PairingProfile(
            name=name,
            description=description,
            enabled=enabled,
            agent_software_release=ven_version,
            allowed_uses_per_key=allowed_uses_per_key,
            key_lifespan=key_lifespan,
            enforcement_mode=enforcement_mode,
            enforcement_mode_lock=enforcement_mode_lock,
            visibility_level=visibility_level,
            visibility_level_lock=visibility_level_lock,
            labels=labels,
            role_label_lock=role_label_lock,
            app_label_lock=app_label_lock,
            env_label_lock=env_label_lock,
            loc_label_lock=loc_label_lock,
            external_data_set=external_data_set,
            external_data_reference=external_data_reference
        )

        if module.check_mode:
            if not existing_profile:
                module.exit_json(changed=True, pairing_profile=pairing_profile_api.json_output(new_profile))
            module.exit_json(
                changed=not pairing_profile_api.params_match(existing_profile),
                pairing_profile=pairing_profile_api.json_output(new_profile)
            )

        if not existing_profile:
            profile = pairing_profile_api.create(new_profile)
            changed = True
        else:
            changed = pairing_profile_api.update(existing_profile, new_profile)
            profile = pairing_profile_api.get_by_href(existing_profile.href) if changed else existing_profile
    elif state == 'absent':
        if module.check_mode:
            module.exit_json(changed=True, pairing_profile={})

        changed = pairing_profile_api.delete(existing_profile)
        profile = {}

    module.exit_json(changed=changed, pairing_profile=pairing_profile_api.json_output(profile))


if __name__ == '__main__':
    main()
