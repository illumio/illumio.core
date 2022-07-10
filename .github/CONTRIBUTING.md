# How to contribute  

## GitHub workflow  

Suggested contribution workflow (feature branching):

1. Create your own fork of the project
2. Create a new branch on the fork
3. Develop the change in your local branch
4. When you're ready to create a pull request, merge the upstream main branch into your local main
5. Merge any changes to the local main branch into your feature branch
6. Merge your feature branch into local main
7. Submit a pull request from your local main branch  

### Open a Pull Request  

Pull requests please follow the standard GitHub PR process.  

### Sign the CLA  

When submitting a pull request, you will be prompted to to sign the Illumio [Contributor License Agreement](CLA.md). The signature is then stored remotely so the process only needs to be completed once.  

## Testing  

Make sure to add unit tests to cover any new functionality. When making changes to existing code, add any necessary regression tests, and/or change existing tests where needed.  

Run tests with ```ansible-test```. It's recommended to install python environments with [`pyenv`](https://github.com/pyenv/pyenv) and install the [`tox-pyenv` library](https://pypi.org/project/tox-pyenv/) to test against multiple versions at once.  

### Integration Tests  

To run the collection's integration tests, you will need to set the following environment variables to establish a connection to your PCE instance:  

Environment variable       | Description         | Default
-------------------------- | ------------------- | -------
`ILLUMIO_PCE_HOST`         | PCE hostname or URL | -
`ILLUMIO_PCE_PORT`         | PCE HTTP(S) port    | `443`
`ILLUMIO_PCE_ORG_ID`       | PCE organization ID | `1`
`ILLUMIO_API_KEY_USERNAME` | PCE API key ID      | -
`ILLUMIO_API_KEY_SECRET`   | PCE API key secret  | -

Then, run the `tests/utils/render_config_templates.sh` script to generate a copy of `integration_config.yml` with the PCE connection values.  

> **NOTE:** the integration test suites make a large number of API calls and create database objects that are not cleaned up automatically. **Do not** run integration tests against a production Policy Compute Engine.  

You can run the integration test suite with  

```sh
ansible-test integration
```

### Sanity Tests  

Sanity tests are automatically run for `ansible>=2.9` and `python>=3.6` through the `.github/workflows/sanity.yml` action. You can run local sanity tests using `ansible-test sanity` to make sure your changes adhere to Ansible style standards.  

This project also adheres to [`ansible-lint`](https://ansible-lint.readthedocs.io/en/latest/) standards.  

## Documentation  

### Project documentation  

* Update the [README](../README.md) if you've added new modules, plugins, roles, or other functionality
* Update the [CHANGELOG](../CHANGELOG.rst)

### Code documentation  

* If you've updated or added a new role, make sure your changes are included under `docs/`. Add a symbolic link from the role directory to the docs md file
* Make sure documentation follows the [Ansible style guide](https://docs.ansible.com/ansible/latest/dev_guide/style_guide/index.html)
* Plugins and modules should have documentation and examples at the top of their python files
