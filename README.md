# Ansible Collection - illumio.illumio  

- [Overview](#overview)
- [Installation](#installation)
    - [Requirements](#requirements)
    - [Ansible Galaxy](#ansible-galaxy)
- [Collection Contents](#collection-contents)
    - [Roles](#roles)
- [Support](#support)
- [License](#license)

## Overview  

This repository contains the official `illumio.illumio` Ansible Collection.  

The collection provides Ansible plugins and roles to automate Virtual Enforcement Node (VEN) installation for the Illumio Policy Compute Engine (PCE).  

## Collection Contents  

### Roles

- [ven](docs/VEN_ROLE.md)
- [kubelink](docs/KUBELINK_ROLE.md)

## Installation  

### Requirements  

This collection has been tested against Ansible **2.9+**.  

Python version **3.6** or higher is required for this collection.

> **Note:** the minimum Python version has been bumped to **3.8** as of Ansible version **2.11+**

In Ansible 2.10 and higher, modules have been moved into collections. Additional collections beyond `ansible.builtin` must now be installed explicitly. The `illumio.illumio` collection depends on the following collections:  

- `community.general`
- `ansible.windows`
- `kubernetes.core`

> **Note:** these dependencies are specified in `galaxy.xml` and will automatically be installed along with the `illumio.illumio` collection  

### Ansible Galaxy  

You can install this collection from Ansible Galaxy using the CLI:  

```sh
ansible-galaxy collection install illumio.illumio
```

## Support  

The `illumio.illumio` collection is released and distributed as open source software subject to the included [LICENSE](LICENSE). Illumio has no obligation or responsibility related to the package with respect to support, maintenance, availability, security or otherwise. Please read the entire [LICENSE](LICENSE) for additional information regarding the permissions and limitations. Support is offered on a best-effort basis through the Illumio app integrations team and project contributors.  

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
