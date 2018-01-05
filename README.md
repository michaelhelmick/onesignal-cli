# OneSignal API CLI

Minimal CLI for interfacing with OneSignal API.

## Installation

`python setup.py install`

## Usage

### Authentication

#### Login
`onesignal login`

#### Logout
`onesignal logout`

### Interfacing with API

#### Sync Apps
`onesignal sync_apps`

#### List Apps
`onesignal list_apps`

#### Create App
> Name is required.
`onesignal create_app -n "My App" --gcm_key "abcde12345" --apns_env "production" --apns_p12 ~/Desktop/app.p12`

#### Update App
> All arguments optinal.
`onesignal update_app -n "My App" --gcm_key "abcde12345" --apns_env "production" --apns_p12 ~/Desktop/app.p12`

#### Help
`onesignal --help`
`onesignal update_app --help`
