# Commands

## Client Configuration

The playbook for creating configurations on client updates is available with the
command

```bash
ansible-playbook client_config.yml
```

No Ansible tags are necessary.

The playbook will check if ARouteServer has been initialised on the host machine
under `~/arouteserver`. It will then copy the necessary configurations to that
directory. These configurations have been created partially by hydrating jinja2
templates from the `ix_client.yml` file.

Afterwards, a virtual pip environment is initialised and requirements are
installed. This environment is used to create `ixf.json` and `bird.conf`. The
last part copies these back to the Ansible directory. Note: this could be
changed to instead copy the files back to the `route_server` role, so they're
instantly ready for deployment.

A `members.md` file is also hydrated. Nothing is done with it. This should be
used to deploy an update to the website, `ix.labitat.dk`.

As a final note: `ansible.cfg` no longer asks for the sudo password and will
thus fail. This can be fixed by either supplying the `-k` flag when running that
playbook or by uncommenting the lines.

## Route Server Deployment

Find available tags with

```shell
ansible-playbook route_server.yml --list-tags
```

The following tags are available:

```shell
apt        # update & install required apt packages
bird       # update bird configuration
deploy     # run & deploy everything
interfaces # update network interfaces
never      # prevent tasks like rebooting except on deployment
nftables   # update nftables config
reboot     # reboot target
ping       # test ping connectivity
```

Run a playbook with

```shell
ansible-playbook route_server.yml --tags ping --diff --ask-become-pass -u <user>
```

Where
- `-t | --tags`: Tags to run
- `-D | --diff`: Shows changes made to config file
- `-K | --ask-become-pass`: Escalates to superuser privilege, if needed.
- `-u`: user to authenticate from

Dry-run with `--check` / `-C`, to check if Ansible runs as intended when working on the Ansible roles.

Note: the BIRD configuration file is currently invalid. This makes the playbook
fail. All configuration files can be found in [`roles/route_server/files/`](roles/route_server/files/).


# Architecture

In the main directory is a file, `inventory`, containing a list of all machines.
The host running Ansible is responsible for connecting to these via `ssh`, so
make sure this is possible (example by changing `~/.ssh/config`). Authenticate as
your user.

Here is a sample SSH config that proxy jumps via SSH from your machine on the LabIX peering LAN, connecting to the route server.

```ssh
host labix_route_server
    user <user>
    #hostname 185.0.29.1
    hostname 2001:7f8:149:1ab::6:0247:1
    proxyjump <your machine>
    IdentityFile ~/.ssh/<SSH file>
```


The `ansible.cfg`-file contains default configuration options, but for now points to the Ansible inventory file.

The `route_server.yml` calls the `route_server` role. This in turn calls
`main.yml` in the `./roles/route_server/tasks/` directory. This imports all the
different plays for updating and deploying.
