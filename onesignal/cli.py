# -*- coding: utf-8 -*-
"""Interface with OneSignal API."""

import base64

import click
import requests

from .config import pass_config


@click.group()
@pass_config
@click.pass_context
def cli(ctx, config):
    config.load()

    if not ctx.invoked_subcommand == 'config':
        config._setup()
        config.load()


@cli.command()
@pass_config
@click.password_option()
def login(config, password):
    """Store OneSignal Auth Key."""
    click.echo("Congratulations, you're authenticated!")


@cli.command()
@pass_config
def logout(config):
    """Delete OneSignal config."""
    for key in config.keys():
        del config[key]
    config.save()

    click.echo("Congratulations, you're logged out!")


@cli.command()
@pass_config
@click.pass_context
def sync_apps(ctx, config):
    """Sync OneSignal apps."""
    if not config.get('auth_key'):
        click.echo('Please provide an auth key!')
        return

    response = requests.get(
        'https://onesignal.com/api/v1/apps',
        headers={
            'Authorization': 'Basic {0}'.format(config['auth_key']),
        },
    )
    apps = response.json()

    config['apps'] = []
    for app in apps:
        config['apps'].append({
            'id': app['id'],
            'name': app['name'],
        })

    config.save()
    config.load()


@cli.command()
@pass_config
@click.pass_context
def list_apps(ctx, config):
    """List OneSignal apps."""
    apps = config.get('apps', [])
    if not apps:
        click.echo('Please sync your apps.')

    for app in apps:
        click.echo('{0} ({1})'.format(app['id'], app['name']))


@cli.command()
@pass_config
@click.option('--app_id')
@click.option('--name', '-n', default='')
@click.option('--apns_env', default='')
@click.option('--apns_p12', type=click.File('rb'))
@click.option('--apns_p12_password', default='')
@click.option('--gcm_key', default='')
@click.pass_context
def update_app(ctx, config, app_id, name, apns_env, apns_p12, apns_p12_password, gcm_key):
    """Update OneSignal App."""
    data = {}
    files = {}

    if name:
        data['name'] = name

    if apns_env and apns_p12:
        data['apns_env'] = apns_env
        data['apns_p12_password'] = apns_p12_password
        data['apns_p12'] = base64.b64encode(apns_p12.read())

    if gcm_key:
        data['gcm_key'] = gcm_key

    response = requests.put(
        'https://onesignal.com/api/v1/apps/{0}'.format(app_id),
        data=data,
        files=files,
        headers={
            'Authorization': 'Basic {0}'.format(config['auth_key']),
        },
    )

@cli.command()
@pass_config
@click.option('--name', '-n')
@click.option('--apns_env', default='')
@click.option('--apns_p12', type=click.File('rb'))
@click.option('--apns_p12_password', default='')
@click.option('--gcm_key', default='')
@click.pass_context
def create_app(ctx, config, name, apns_env, apns_p12, apns_p12_password, gcm_key):
    """Create OneSignal App."""
    data = {}

    if name:
        data['name'] = name

    if apns_env and apns_p12:
        data['apns_env'] = apns_env
        data['apns_p12_password'] = apns_p12_password
        data['apns_p12'] = base64.b64encode(apns_p12.read())

    if gcm_key:
        data['gcm_key'] = gcm_key

    response = requests.post(
        'https://onesignal.com/api/v1/apps',
        data=data,
        headers={
            'Authorization': 'Basic {0}'.format(config['auth_key']),
        },
    )

    ctx.invoke(sync_apps)

