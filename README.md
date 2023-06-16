# Ansible Collection - illumio.core  

> **NOTE:** this collection is currently under development, and is **not yet available on Ansible Automation Platform**. If you are interested in learning more about the project, please reach out to the [Illumio Integrations team](mailto:app-integrations@illumio.com).  

- [Overview](#overview)
- [Collection Contents](#collection-contents)
    - [Modules](#modules)
    - [Roles](#roles)
- [Installation](#installation)
    - [Requirements](#requirements)
    - [Ansible Galaxy](#ansible-galaxy)
- [Usage](#usage)
    - [Using illumio Modules](#using-illumio-modules)
    - [Using illumio Roles](#using-illumio-roles)
- [Support](#support)
- [Contributing](#contributing)
- [License](#license)

## Overview  

This repository contains the official `illumio.core` Ansible Collection.  

The collection provides Ansible plugins and roles to automate Virtual Enforcement Node (VEN) installation for the Illumio Policy Compute Engine (PCE).  

## Collection Contents  

### Modules  

- [pairing_profile](plugins/modules/pairing_profile.py)
- [pairing_key](plugins/modules/pairing_key.py)
- [container_cluster](plugins/modules/container_cluster.py)
- [label](plugins/modules/label.py)

### Roles  

- [ven](docs/VEN_ROLE.md)
- [ven_library](docs/VEN_LIBRARY_ROLE.md)
- [kubelink](docs/KUBELINK_ROLE.md)
- [cven](docs/CVEN_ROLE.md)

## Installation  

### Requirements  

Python version **3.8** or higher is required for this collection.  

**Python**  

For most components, you will need the `illumio` Python library version **1.1.3** or higher installed on the Ansible controller:  

```sh
$ pip install illumio>=1.1.3
```

For Windows hosts, you will also need to install the `pywinrm` library on the Ansible controller:

```sh
$ pip install pywinrm
```

**Ansible**  

This collection works with Ansible versions **2.12** and above.  

In Ansible 2.10 and higher, modules have been moved into collections. Additional collections beyond `ansible.builtin` must now be installed explicitly. The `illumio.core` collection depends on the following collections:  

> **Note:** individual modules may have additional requirements beyond these - see the documentation linked in the [Collection Contents](#collection-contents) section above for installation details and requirements.  

- `community.general`
- `ansible.windows`
- `kubernetes.core`

> **Note:** these dependencies are specified in `galaxy.xml` and will automatically be installed along with the `illumio.core` collection  

### Ansible Galaxy  

You can install this collection from Ansible Galaxy using the CLI:  

```sh
ansible-galaxy collection install illumio.core
```

## Usage  

> **NOTE:** these are not fully working examples. See the documentation linked in the [Collection Contents](#collection-contents) section above for usage details for specific modules and roles.  

### Using illumio Modules  

```yml
---
- name: Use the pairing_profile module
  hosts: localhost
  gather_facts: no
  tasks:
  - name: Create pairing profile
    illumio.core.pairing_profile:
      name: PP-ANSIBLE
      enabled: true
      state: present
    register: profile_result

  - name: Generate pairing key
    illumio.core.pairing_key:
      pairing_profile_href: "{{ profile_result.pairing_profile['href'] }}"
    register: result

  - debug:
      var: result.pairing_key
```

### Using illumio Roles  

After downloading the collection or an individual role, you can run them individually using the fully-qualified name:

```yml
---
- name: Pair VEN using the illumio collection
  hosts: localhost
  roles:
    - role: illumio.core.ven
      illumio_pce_hostname: my.pce.com
      ...
```

Or by specifying `illumio.core` in the `collections` field and using the role name as below:

```yml
---
- name: Pair VEN using the illumio collection
  hosts: localhost
  collections:
    - illumio.core

  roles:
    - role: ven
      illumio_pce_hostname: my.pce.com
      ...
```

## Support  

The `illumio.core` collection is released and distributed as open source software subject to the included [LICENSE](LICENSE). Illumio has no obligation or responsibility related to the package with respect to support, maintenance, availability, security or otherwise. Please read the entire [LICENSE](LICENSE) for additional information regarding the permissions and limitations. Support is offered on a best-effort basis through the [Illumio app integrations team](mailto:app-integrations@illumio.com) and project contributors.  

## Contributing  

See the project's [CONTRIBUTING](.github/CONTRIBUTING.md) document for details.  

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
