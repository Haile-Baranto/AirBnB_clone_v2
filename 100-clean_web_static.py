#!/usr/bin/python3
"""A module for web application deployment with Fabric."""
from fabric.api import env, run, runs_once, local
from os import listdir

# Define the hosts and the user for the remote commands
env.hosts = ['xx-web-01', 'xx-web-02']
env.user = 'ubuntu'


@runs_once
def do_clean(number=0):
    """Delete out-of-date archives."""
    # Convert the number argument to an integer
    number = int(number)
    # Get the list of archive files in the versions folder
    files = sorted(listdir("versions"))
    # If number is 0 or 1, keep only the most recent version of your archive
    if number <= 1:
        number = 1
    # Delete all unnecessary archives in the versions folder
    for file in files[:-number]:
        local("rm versions/{}".format(file))
    # Get the list of archive folders in the /data/web_static/releases
    # folder of both web servers
    folders = sorted(run("ls -tr /data/web_static/releases").split())
    # Delete all unnecessary archives in the /data/web_static/releases
    # folder of both web servers
    for folder in folders[:-number]:
        run("rm -rf /data/web_static/releases/{}".format(folder))
