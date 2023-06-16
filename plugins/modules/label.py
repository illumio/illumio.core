#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2023 Illumio, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: label
short_description: Create/update/delete Illumio PCE labels
description:
  - This module allows you to create and manipulate label objects on the Illumio PCE.
  - Supports check mode.

author:
  - Duncan Sommerville (@dsommerville-illumio)
requirements:
  - "python>=3.8"
  - "illumio>=1.1.3"
version_added: "0.3.0"

options:
  href:
    description: HREF of an existing label.
    type: str
  key:
    description:
      - Label dimension key.
      - Required for creating a label or when HREF is not specified.
    type: str
  value:
    description:
      - Label name in the PCE.
      - Required for creating a label or when HREF is not specified.
    type: str
  state:
    description:
      - Desired label state.
      - If C(present), the label will be created if it does not exist, or updated to match the provided parameters if it does.
      - If C(absent), the label will be removed if it exists.
    type: str
    choices: ['present', 'absent']
    default: 'present'
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
- name: "Create Test env label"
  illumio.core.label:
    key: env
    value: Test
    state: present

- name: "Remove existing label"
  illumio.core.label:
    key: env
    value: Test
    state: absent

- name: "Remove label by HREF"
  illumio.core.label:
    href: /orgs/1/labels/1
    state: absent
'''

RETURN = r'''
label:
  description: Information about the label that was created or updated.
  type: complex
  returned: success
  contains:
    href:
      description: The label's HREF.
      type: str
      returned: always
    key:
      description: The label key.
      type: str
      returned: always
    value:
      description: The label value.
      type: str
      returned: always
    deleted:
      description: Flag denoting whether or not the label has been deleted on the PCE.
      type: bool
      returned: always
    external_data_set:
      description: External data set identifier.
      type: str
      returned: always
    external_data_reference:
      description: External data reference identifier.
      type: str
      returned: always
    created_at:
      description: A timestamp denoting when this label was created.
      type: str
      returned: always
    created_by:
      description: A reference to the user object that created this label.
      type: dict
      returned: always
      sample:
        created_by:
          href: /users/1
    updated_at:
      description: A timestamp denoting when this label was last updated.
      type: str
      returned: always
    updated_by:
      description: A reference to the user object that last updated this label.
      type: dict
      returned: always
      sample:
        updated_by:
          href: /users/1

  sample:
    label:
      href: /orgs/1/label/1500
      key: loc
      value: AWS
      created_at: "2022-06-07T00:11:10.923Z"
      created_by:
        href: /users/1
      updated_at: "2022-06-07T17:51:56.606Z"
      updated_by:
        href: /users/1
'''

import sys
import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.illumio.core.plugins.module_utils.pce import PceObjectApi, pce_connection_spec  # type: ignore

IMPORT_ERROR_TRACEBACK = ''

try:
    from illumio import Label
except ImportError:
    Label = None
    # replicate the traceback formatting from AnsibleModule.fail_json
    IMPORT_ERROR_TRACEBACK = ''.join(traceback.format_tb(sys.exc_info()[2]))


class LabelApi(PceObjectApi):
    def __init__(self, module: AnsibleModule) -> None:
        super().__init__(module)
        self._api = self._pce.labels

    def params_match(self, o):
        ignore_params = ['href', 'state']
        params = [k for k in spec().keys() if k not in ignore_params]
        for k in params:
            if self._module.params.get(k) != getattr(o, k, None):
                return False
        return True


def spec():
    return dict(
        href=dict(type='str'),
        # explicitly set no_log to false to avoid ansible-lint false positive
        # see https://docs.ansible.com/ansible-core/devel/dev_guide/testing/sanity/validate-modules.html
        key=dict(type='str', no_log=False),
        value=dict(type='str'),
        state=dict(
            type='str',
            choices=['present', 'absent'],
            default='present'
        ),
        external_data_set=dict(type='str'),
        external_data_reference=dict(type='str')
    )


def main():
    argument_spec = pce_connection_spec()
    argument_spec.update(spec())

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[['key', 'href']],
        required_together=[
            ['key', 'value'],
            ['external_data_set', 'external_data_reference'],
        ],
        supports_check_mode=True
    )

    if not Label:
        module.fail_json(
            msg=missing_required_lib('illumio', url='https://pypi.org/project/illumio/'),
            exception=IMPORT_ERROR_TRACEBACK
        )

    label_api = LabelApi(module)

    href = module.params.get('href')
    key = module.params.get('key')
    value = module.params.get('value')
    state = module.params.get('state')
    external_data_set = module.params.get('external_data_set')
    external_data_reference = module.params.get('external_data_reference')

    if href:
        existing_label = label_api.get_by_href(href)
        if not existing_label:
            module.fail_json("No label found with HREF %s" % (href))
    elif key:
        existing_label = label_api.get_one({'key': key, 'value': value})

    if state == 'present':
        new_label = Label(
            key=key,
            value=value,
            external_data_set=external_data_set,
            external_data_reference=external_data_reference
        )

        if module.check_mode:
            if not existing_label:
                module.exit_json(changed=True, label=label_api.json_output(new_label))
            module.exit_json(
                changed=not label_api.params_match(existing_label),
                label=label_api.json_output(new_label)
            )

        if not existing_label:
            label = label_api.create(new_label)
            changed = True
        elif existing_label.deleted or (not new_label.key and not new_label.value):
            module.exit_json(changed=False, label=label_api.json_output(existing_label))
        else:
            # label key can't be changed once it's created
            if new_label.key != existing_label.key:
                module.fail_json("Unable to update key of existing label")
            new_label.key = None  # null the key so it isn't passed in the request
            changed = label_api.update(existing_label, new_label)
            label = label_api.get_by_href(existing_label.href) if changed else existing_label
    elif state == 'absent':
        if module.check_mode:
            module.exit_json(changed=True, label={})

        if not existing_label or existing_label.deleted:
            module.exit_json(changed=False, label={})

        changed = label_api.delete(existing_label)
        label = {}

    module.exit_json(changed=changed, label=label_api.json_output(label))


if __name__ == '__main__':
    main()
