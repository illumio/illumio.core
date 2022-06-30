#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2022 Illumio, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: container_cluster
short_description: Create/update/delete Illumio PCE container clusters
description:
    - This module allows you to create and manipulate container cluster objects on the Illumio PCE to sync with Kubernetes or OpenShift clusters.
    - Only the name and description values for the cluster can be set when creating or updating a cluster.
    - All other values are computed based on the sync data from a Kubelink pod installed in the cluster.
    - See https://docs.illumio.com/core/21.5/Content/Guides/kubernetes-and-openshift/deployment/deploy-kubelink-in-your-cluster.htm
author:
  - Duncan Sommerville (@dsommerville-illumio)
requirements:
  - "python>=3.6"
  - "illumio>=1.0.1"
version_added: "0.2.0"

options:
    href:
        description: HREF of an existing container cluster.
        type: str
    name:
        description:
            - Container cluster display name.
            - Required for creating a container cluster or when HREF is not specified.
        type: str
    description:
        description: Container cluster description.
        type: str
    state:
        description:
            - Desired container cluster state.
            - If C(present), the cluster will be created if it does not exist, or updated to match the provided parameters if it does.
            - If C(absent), the cluster will be removed if it exists.
        type: str
        choices: ['present', 'absent']
        default: 'present'

extends_documentation_fragment:
  - illumio.illumio.pce
'''

EXAMPLES = r'''
- name: "Create container cluster"
  illumio.illumio.container_cluster:
    name: CC-KUBE
    description: Kubernetes cluster
    state: present
  register: container_cluster_result

- name: "Store container cluster token"
  set_fact:
    kube_cluster_token: "{{ container_cluster_result.container_cluster['container_cluster_token'] }}"

- name: "Remove existing cluster"
  illumio.illumio.pairing_profile:
    name: CC-KUBE
    state: absent

- name: "Remove cluster by HREF"
  illumio.illumio.pairing_profile:
    href: /orgs/1/container_clusters/f5bef182-8c55-4219-b35b-0a50b707e434
    state: absent
'''

RETURN = r'''
container_cluster:
    description: Information about the container cluster that was created or updated.
    type: complex
    returned: success
    contains:
        href:
            description: The container cluster's HREF.
            type: str
            returned: always
        name:
            description: The container cluster's name.
            type: str
            returned: always
        description:
            description: A description of the container cluster.
            type: str
            returned: always
        pce_fqdn:
            description: PCE fully-qualified domain name.
            type: str
            returned: always
        manager_type:
            description: Container cluster type and version.
            type: str
            returned: always
            sample: Kubernetes v1.24.1
        last_connected:
            description: ISO date-timestamp of the last heartbeat from the container cluster to the PCE.
            type: str
            returned: always
            sample: 2022-06-23T20:53:57.885Z
        kubelink_version:
            description: Version of the Kubelink software used to pair this cluster to the PCE.
            type: str
            returned: always
            sample: 2.0.2.d53d7f
        online:
            description: Whether or not the container cluster is online.
            type: bool
            returned: always
        nodes:
            description: List of node names and pod subnets belonging to the cluster.
            type: list
            elements: dict
            suboptions:
                name:
                    description: The cluster node name.
                    type: str
                    returned: always
                pod_subnet:
                    description: The cluster node's pod subnet range
                    type: str
                    returned: always
            default: []
            returned: always
            sample: [
                {
                    "name": "kube-leader",
                    "pod_subnet": "192.168.0.0/24"
                }
            ]
        container_runtime:
            description: Default container runtime for the cluster.
            type: str
            returned: always
            sample: containerd
        errors:
            description: List of errors to do with the container cluster.
            type: list
            elements: dict
            suboptions:
                audit_event:
                    description: The audit event object associated with this error.
                    type: dict
                    suboptions:
                        href:
                            description: The HREF of the audit event object.
                            type: str
                            returned: always
                    returned: always
                duplicate_ids:
                    description: Duplicate error IDs.
                    type: list
                    elements: str
                    returned: always
                error_type:
                    description: Error type.
                    type: str
                    returned: always
            default: []
            returned: always
            sample: [
                {
                    "audit_event": {
                        "href": "string"
                    },
                    "duplicate_ids": [],
                    "error_type": "string"
                }
            ]
        caps:
            description:
                - Array of permissions on the entity held by the requesting user.
                - An empty array implies readonly permission.
            type: list
            elements: str
            default: []
            returned: always
        container_cluster_token:
            description:
                - The pairing token for the cluster.
                - This token is only returned once when the cluster is created.
                - It cannot be retrieved through the API after this, so make sure to store it in a secure, persistent form.
            type: str
            returned: on successful creation

    sample: {
        "href": "/orgs/1/container_clusters/f5bef182-8c55-4219-b35b-0a50b707e434",
        "pce_fqdn": null,
        "name": "CC-EKS-LAB",
        "description": "Lab Kubernetes cluster in AWS",
        "manager_type": "Kubernetes v1.24.1",
        "last_connected": "2022-06-23T20:53:57.885Z",
        "kubelink_version": "2.0.2.d53d7f",
        "online": true,
        "nodes": [
            {
                "name": "kube-leader",
                "pod_subnet": "192.168.0.0/24"
            }
        ],
        "container_runtime": "containerd",
        "errors": [],
        "caps": ["write"],
        "container_cluster_token": "1_0dfec0acb8e4bc53e052874874da0c24e7ac98da3b3954e3c9ea6f9860722e84"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.illumio.illumio.plugins.module_utils.pce import PceObjectApi, pce_connection_spec  # type: ignore

from illumio.infrastructure import ContainerCluster


class ContainerClusterApi(PceObjectApi):
    def __init__(self, module: AnsibleModule) -> None:
        super().__init__(module)
        self._api = self._pce.container_clusters

    def params_match(self, cluster):
        return self._module.params.get('name') == getattr(cluster, 'name', None) \
            and self._module.params.get('description') == getattr(cluster, 'description', None)


def spec():
    return dict(
        href=dict(type='str'),
        name=dict(type='str'),
        description=dict(type='str', default=''),
        state=dict(
            type='str',
            choices=['present', 'absent'],
            default='present'
        )
    )


def main():
    argument_spec = pce_connection_spec()
    argument_spec.update(spec())

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[['name', 'href']],
        supports_check_mode=True
    )

    container_cluster_api = ContainerClusterApi(module)

    href = module.params.get('href')
    name = module.params.get('name')
    description = module.params.get('description')
    state = module.params.get('state')

    if href:
        existing_cluster = container_cluster_api.get_by_href(href)
        if not existing_cluster:
            module.fail_json("No container cluster found with HREF %s" % (href))
    elif name:
        existing_cluster = container_cluster_api.get_by_name(name)

    if state == 'present':
        new_cluster = ContainerCluster(
            name=name,
            description=description
        )

        if module.check_mode:
            if not existing_cluster:
                module.exit_json(changed=True, container_cluster=container_cluster_api.json_output(new_cluster))
            module.exit_json(
                changed=not container_cluster_api.params_match(existing_cluster),
                container_cluster=container_cluster_api.json_output(new_cluster)
            )

        if not existing_cluster:
            cluster = container_cluster_api.create(new_cluster)
            changed = True
        else:
            changed = container_cluster_api.update(existing_cluster, new_cluster)
            cluster = container_cluster_api.get_by_href(existing_cluster.href) if changed else existing_cluster
    elif state == 'absent':
        if module.check_mode:
            module.exit_json(changed=True, container_cluster={})

        changed = container_cluster_api.delete(existing_cluster)
        cluster = {}

    module.exit_json(changed=changed, container_cluster=container_cluster_api.json_output(cluster))


if __name__ == '__main__':
    main()
