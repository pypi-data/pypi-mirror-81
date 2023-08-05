from expects import *

from sym.cli.helpers.ansible import get_ansible_bucket_name
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.tests.commands.test_ansible import TEST_ACCOUNT, get_caller_identity_stub


def test_get_ansible_bucket_name(
    boto_stub,
    saml_client: SAMLClient,
):
    get_caller_identity_stub(boto_stub)
    actual = get_ansible_bucket_name(saml_client)
    expect(actual).to(match(f"sym-ansible-{TEST_ACCOUNT}"))
