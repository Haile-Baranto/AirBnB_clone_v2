#!/usr/bin/python3
# Fabric script that creates and distributes an archive to web servers

from fabric.api import env, put, run, runs_once, local
from os.path import exists
from datetime import datetime

# Define the hosts and the user for the remote commands
env.hosts = ['xx-web-01', 'xx-web-02']
env.user = 'ubuntu'


@runs_once
def do_pack():
    """Create a .tgz archive from the web_static folder."""
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")
    # Get the current date and time in the format yearmonthdayhourminutesecond
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    # Create the archive name using the web_static prefix and the date and time
    archive_name = "web_static_{}.tgz".format(now)
    # Create the archive using the tar command with the options -cvzf
    # The archive should be stored in the versions folder
    result = local("tar -cvzf versions/{} web_static".format(archive_name))
    # If the archive was created successfully, return the path of the archive
    # Otherwise, return None
    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None


def do_deploy(archive_path):
    """Distribute an archive to web servers."""
    # Return False if the file at the path archive_path doesn't exist
    if not exists(archive_path):
        return False
    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/")
    # Get the archive filename without extension
    filename = archive_path.split("/")[-1].split(".")[0]
    # Create the folder /data/web_static/releases/<archive filename
    # without extension> on the web server
    run("mkdir -p /data/web_static/releases/{}/".format(filename))
    # Uncompress the archive to that folder on the web server
    run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/".format(
        filename, filename))
    # Delete the archive from the web server
    run("rm /tmp/{}.tgz".format(filename))
    # Delete the symbolic link /data/web_static/current from the web server
    run("rm -rf /data/web_static/current")
    # Create a new symbolic link /data/web_static/current on the web server,
    # linked to the new version of your code
    run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(
        filename))
    # Return True if all operations have been done correctly,
    # otherwise return False
    return True


def deploy():
    """Create and distribute an archive to web servers."""
    # Call the do_pack() function and store the path of the created archive
    archive_path = do_pack()
    # Return False if no archive has been created
    if not archive_path:
        return False
    # Call the do_deploy(archive_path) function, using the new path of
    # the new archive
    result = do_deploy(archive_path)
    # Return the return value of do_deploy
    return result
