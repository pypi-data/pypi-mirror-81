'''
Entry point for cli utility
'''

import click
import pkg_resources
import requests
import yaml
from matatika.config import MatatikaConfig
from matatika.exceptions import WorkspaceNotFoundError
from matatika.exceptions import MatatikaException
from matatika.dataset_fields import DatasetItems
from matatika.library import MatatikaClient

version = pkg_resources.require("matatika")[0].version


@click.group()
@click.version_option(version=version)

def start(): # pylint: disable=missing-function-docstring
    pass

@start.command('publish', short_help='Publish one or more dataset(s)')
@click.option('--workspace-id', '-w', type=click.UUID, help='Workspace ID')
# There is a type for file & path - we will loo into that option
@click.option('--dataset', '-f', type=click.Path(exists=True),required=True, help='Dataset file')
@click.option('--auth-token', '-a', help='Authorisation token')
@click.option('--endpoint-url', '-u', help='Endpoint URL')
def publish(workspace_id, dataset, auth_token, endpoint_url):
    '''
    Publish one or more dataset(s) from a YAML file to a workspace

    Usage example:\n
        matatika publish -w ea30ef68-3fd8-4200-80c5-5d322af1ab07 -d dataset.yaml -a $AUTH_TOKEN

    '''

    # if non-required options are not provided, retrieve them from the config file
    config = MatatikaConfig()
    if workspace_id is None:
        workspace_id = config.get_default_workspace()
    if auth_token is None:
        auth_token = config.get_auth_token()
    if endpoint_url is None:
        endpoint_url = config.get_endpoint_url()

    client = MatatikaClient(auth_token, endpoint_url, workspace_id)

    with open(dataset, 'r') as datasets_file:
        datasets_yaml_obj = yaml.safe_load(datasets_file)
        datasets = datasets_yaml_obj[DatasetItems.DATASETS.value]

    try:
        client.publish(datasets)
        click.secho("Published successfully", fg='green')

    except requests.HTTPError as err:
        click.secho(str(err), fg='red')

        status_code = err.response.status_code
        if status_code == 401:
            click.secho("Please check your auth token is correct and valid", fg='red')

    except WorkspaceNotFoundError as err:
        click.secho(str(err), fg='red')




@start.command('list', short_help='List of available workspaces')
@click.option('--auth_token', '-a', help='Authorization token')
@click.option('--endpoint-url', '-u', help='Endpoint URL')
def list_(auth_token, endpoint_url):
    '''
    Display a list of all available workspaces
    Usage example:\n
            matatika list
    '''

    # if non-required options are not provided, retrieve them from the config file
    config = MatatikaConfig()
    if auth_token is None:
        auth_token = config.get_auth_token()
    if endpoint_url is None:
        endpoint_url = config.get_endpoint_url()

    client = MatatikaClient(auth_token, endpoint_url, None)

    try:
        workspaces = client.list_workspaces()

        click.echo("{:<36}{:4}{:<36}".format("WORKSPACE ID", " ", "NAME"))
        for workspace in workspaces:
            click.echo("{:<36}{:4}{:<36}".format(workspace['id'], " ", workspace['name']))

        click.echo("\nTotal workspaces: {}".format(len(workspaces)))

    except requests.HTTPError as err:
        click.secho(str(err), fg='red')
        click.secho("Please check your auth token is correct and valid", fg='red')

    except KeyError:
        click.secho("No workspaces found", fg='red')


@start.command('use', short_help='View or set the default workspace')
@click.option('--workspace-id', '-w', type=click.UUID, help='Authorisation token')
def use(workspace_id):
    '''
    View or set the workspace used by default in other CLI commands

    View the default workspace:\n
        matatika use

    Set the default workspace:\n
        matatika use -w $WORKSPACE_ID
    '''

    config = MatatikaConfig()

    auth_token = config.get_auth_token()
    endpoint_url = config.get_endpoint_url()

    client = MatatikaClient(auth_token, endpoint_url, None)

    try:
        if workspace_id:
            workspace_id = str(workspace_id)

            workspaces = client.list_workspaces()

            workspace_ids = [workspaces[i]['id'] for i in range(len(workspaces))]

            if workspace_id not in workspace_ids:
                raise WorkspaceNotFoundError(workspace_id)

            config.set_default_workspace(workspace_id)

        workspace_context = config.get_default_workspace()

        if workspace_context:
            click.secho("Workspace context set to {}".format(workspace_context), fg='green')
        else:
            click.secho("No workspace context set")

    except requests.HTTPError as err:
        click.secho(str(err), fg='red')
        click.secho("Please check your auth token is correct and valid", fg='red')
    except WorkspaceNotFoundError as err:
        click.secho(str(err), fg='red')
    except MatatikaException as err:
        click.secho(str(err), fg='red')


@start.command('login', short_help='Login to a Matatika account')
@click.option('--auth-token', '-a', required=True, help='Authorisation token')
def login(auth_token):
    '''
    Log in to a Matatika account using an auth token

    Usage:\n
        matatika login $AUTH_TOKEN
    '''

    config = MatatikaConfig()

    config.set_auth_token(auth_token)

    click.secho("Authentication context set", fg='green')

@start.command('endpoint', short_help='View or set the endpoint URL')
@click.option('--url', '-u', help='Endpoint URL')
def endpoint(url):
    '''
    View or set the endpoint URL other commands run against

    View the endpoint URL:\n
        matatika endpoint

    Set the endpoint URL:\n
        matatika endpoint
    '''
    config = MatatikaConfig()

    if url:
        config.set_endpoint_url(url)

    try:
        endpoint_url = config.get_endpoint_url()
        click.secho("Endpoint URL set to {}".format(endpoint_url), fg='green')

    except KeyError:
        click.secho("No endpoint URL set", fg='red')


if __name__ == '__main__':
    start()
