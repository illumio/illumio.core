# illumio.illumio.ven_library role  

- [Host Requirements](#host-requirements)
    - [Operating System](#operating-system)
    - [VEN Compatibility](#ven-compatibility)
- [Installation](#installation)
    - [Requirements](#requirements)
- [Usage Examples](#usage-examples)
- [Role Variables](#role-variables)
    - [VEN Bundle](#ven-bundle)
- [License](#license)

## Host Requirements  

### Operating System  

This role will work with the following operating systems:

- CentOS
- Red Hat Enterprise Linux

See the PCE compatibility chart for details.

### VEN Compatibility  

PCE Version  | VEN 21.2.5 | VEN 21.5.20
------------ | :--------: | :---------: 
21.2         | X          | 
21.5         | X          | X

See the [Illumio Support dependencies page](https://support.illumio.com/software/os-support-package-dependencies/ven.html) for specific VEN OS compatibility details.  

## Installation  

You can install this role with: `ansible-galaxy install illumio.illumio.ven_library`

### Requirements  

To use this role, you will need a VEN bundle and VEN upgrade Compatibility Matrix bundles on the Ansible host system. These `.bz2` bundles can be downloaded from the [Illumio Support Portal download page](https://support.illumio.com/software/download.html).  
For details, see [VEN Library Setup in the PCE](https://docs.illumio.com/core/21.5/Content/Guides/ven-install-upgrade/set-up-pce/ven-library-setup-in-the-pce.htm) in the _VEN Install and Upgrade_ guide.  

> **Note:** these dependencies are included when installing the `illumio` collection with `ansible-galaxy collection install illumio.illumio`  

## Usage Examples  

**Example inventory file**  

```ini
[pces]
10.0.9.212   ansible_connection=ssh  ansible_user=jdoe

[pces:vars]
illumio_ven_bundle_path="/usr/john.doe/illumio/ven/21.5/illumio-ven-bundle-21.5.xx-xxxx.tar.bz2"
illumio_compatibility_matrix_path="/usr/john.doe/illumio/ven/21.5/illumio-release-compatibility-21-xxx.tar.bz2"
```

**Example playbook**  

```yml
---
- name: "Install VEN version 21.5"
  hosts: pces
  gather_facts: yes
  roles:
    - role: illumio.illumio.ven_library
```

## Role Variables  

### VEN Bundle  

Variable | Description | Default value
-------- | ----------- | -------------
`illumio_ven_bundle_path` | Absolute path to the VEN `.bz2` bundle on the Ansible host | -
`illumio_compatibility_matrix_path` | Absolute path to the compatibility matrix `.bz2` bundle on the Ansible host | -
`remote_ven_bundle_path` | Absolute path to the location on the remote to copy the VEN bundle | `/tmp/illumio_ansible_ven_library_ven_bundle.tar.bz2`
`remote_compatibility_matrix_path` | Absolute path to the location on the remote to copy the compatibility matrix bundle | `/tmp/illumio_ansible_ven_library_compatibility_matrix.tar.bz2`
`illumio_ven_library_orgs_list` | Comma-separated list of orgs to install this VEN to | `all`
`illumio_ven_library_set_default` | If `yes`, sets this VEN version as the default for the PCE | `no`
`illumio_pce_user` | The Illumio PCE service user | `ilo-pce`

## License  

Copyright 2022 Illumio  

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
