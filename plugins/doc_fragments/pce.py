# -*- coding: utf-8 -*-

# Copyright 2022 Illumio, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
  pce_hostname:
    description:
      - URL or FQDN of Illumio Policy Compute Engine.
        C(pce_url) is an alias for C(pce_hostname).
      - Can be set with the environment variable C(ILLUMIO_PCE_HOST).
    type: str
    aliases: [ pce_url ]
    required: true
  pce_port:
    description:
      - HTTP(S) port used by the PCE.
      - Can be set with the environment variable C(ILLUMIO_PCE_PORT).
    type: int
    default: 443
  pce_org_id:
    description:
      - PCE Organization ID.
      - Can be set with the environment variable C(ILLUMIO_PCE_ORG_ID).
    type: int
    default: 1
  api_key_username:
    description:
      - Illumio PCE API key username.
      - Can be set with the environment variable C(ILLUMIO_API_KEY_USERNAME).
    type: str
    required: true
  api_key_secret:
    description:
      - Illumio PCE API key secret.
      - Can be set with the environment variable C(ILLUMIO_API_KEY_SECRET).
    type: str
    required: true
  pce_tls_verify:
    description:
      - Flag denoting whether TLS verification should be enabled on the PCE connection.
    type: bool
    default: true
  pce_tls_ca:
    description:
      - Path to a custom root CA certificate bundle to use for the PCE connection.
      - If set, overrides C(pce_tls_verify).
    type: str
  pce_tls_client_certs:
    description:
      - Optional paths to client-side certificate files.
      - May point to separate cert and private key files or a PEM bundle containing both.
    type: list
    elements: str
  pce_http_proxy:
    description:
      - HTTP proxy server to use when connecting to the PCE.
      - If not set, it will use the default C(http_proxy) environment variable.
    type: str
  pce_https_proxy:
    description:
      - HTTPS proxy server to use when connecting to the PCE.
      - If not set, it will use the default C(https_proxy) environment variable.
    type: str
'''
