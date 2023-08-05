import json
import pytest
import requests
import unittest
from click.testing import CliRunner
from matatika.cli import start
from matatika.config import MatatikaConfig

class TestCLI(unittest.TestCase):

    config = MatatikaConfig()

    def setUp(self):
        self.runner = CliRunner()
        

    def tearDown(self):
        pass
    

    # login
    def test_login_with_no_opts(self):
        result = self.runner.invoke(start, ["login"])

        self.assertIn("Error: Missing option '--auth-token' / '-a'", result.output)
        self.assertIs(result.exit_code, 2)

    def test_login_with_empty_opts(self):
        result = self.runner.invoke(start, ["login", "-a"])
        
        self.assertIn("Error: -a option requires an argument", result.output)
        self.assertIs(result.exit_code, 2)

    def test_login_with_auth_token_opt(self):
        result = self.runner.invoke(start, ["login", "-a", "auth-token"])
        
        self.assertIn("Authentication context set", result.output)
        self.assertIs(result.exit_code, 0)


    # endpoint
    def test_endpoint_with_no_opts(self):
        endpoint_url = "some-endpoint-url"
        TestCLI.config.set_endpoint_url(endpoint_url)

        result = self.runner.invoke(start, ["endpoint"])

        self.assertIn("Endpoint URL set to {}".format(endpoint_url), result.output)
        self.assertIs(result.exit_code, 0)

    def test_endpoint_with_empty_opts(self):
        result = self.runner.invoke(start, ["endpoint", "-u"])
        
        self.assertIn("Error: -u option requires an argument", result.output)
        self.assertIs(result.exit_code, 2)

    def test_endpoint_with_endpoint_url_opt(self):
        endpoint_url = "endpoint url"
        result = self.runner.invoke(start, ["endpoint", "-u", endpoint_url])
        
        self.assertIn("Endpoint URL set to {}".format(endpoint_url), result.output)
        self.assertIs(result.exit_code, 0)


    # use
    def test_use_with_no_opts(self):
        default_workspace_id = "default-workspace-id"
        TestCLI.config.set_default_workspace(default_workspace_id)

        result = self.runner.invoke(start, ["use"])
        self.assertIn("Workspace context set to {}".format(default_workspace_id), result.output)
        self.assertIs(result.exit_code, 0)

    def test_use_with_workspace_id_opt_as_invalid_uuid(self):
        invalid_uuid = "this-is-not-a-valid-uuid-string"
        result = self.runner.invoke(start, ["use", "-w", invalid_uuid])
        self.assertIn("Invalid value for '--workspace-id' / '-w': {} is not a valid UUID value".format(invalid_uuid), result.output)
        self.assertIs(result.exit_code, 2)

    def test_use_with_workspace_id_opt_as_invalid_workspace_id(self):
        # requires mock context implementation
        pass
    
    def test_use_with_valid_workspace_id_opt(self):
        # requires mock context implementation
        pass

    # list
    def test_list_with_no_opts(self):
        # requires mock context implementation
        pass

    def test_list_with_empty_opts(self):
        result = self.runner.invoke(start, ["list", "-a"])
        self.assertIn("Error: -a option requires an argument", result.output)
        self.assertIs(result.exit_code, 2)

        result = self.runner.invoke(start, ["list", "-u"])
        self.assertIn("Error: -u option requires an argument", result.output)
        self.assertIs(result.exit_code, 2)

    def test_list_with_auth_token_opt(self):
        # requires mock context implementation
        pass

    def test_list_with_endpoint_url_opt(self):
        # requires mock context implementation
        pass

    def test_list_with_all_opts(self):
        # requires mock context implementation
        pass

    # list
    def test_publish_with_no_opts(self):
        result = self.runner.invoke(start, ["publish"])

        self.assertIn("Error: Missing option '--dataset' / '-f'", result.output)
        self.assertIs(result.exit_code, 2)

    def test_publish_with_empty_opts(self):
        result = self.runner.invoke(start, ["publish", "-w"])
        self.assertIn("Error: -w option requires an argument", result.output)
        self.assertIs(result.exit_code, 2)

        result = self.runner.invoke(start, ["publish", "-f"])
        self.assertIn("Error: -f option requires an argument", result.output)
        self.assertIs(result.exit_code, 2)

        result = self.runner.invoke(start, ["publish", "-a"])
        self.assertIn("Error: -a option requires an argument", result.output)
        self.assertIs(result.exit_code, 2)

        result = self.runner.invoke(start, ["publish", "-u"])
        self.assertIn("Error: -u option requires an argument", result.output)
        self.assertIs(result.exit_code, 2)

    def test_publish_with_dataset_opt_as_invalid_path(self):
        invalid_path = "this-is-not-a-valid-path"
        result = self.runner.invoke(start, ["publish", "-f", invalid_path])
        self.assertIn("Invalid value for '--dataset' / '-f': Path '{}' does not exist".format(invalid_path), result.output)
        self.assertIs(result.exit_code, 2)