#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the web_static folder

from fabric.api import local
from datetime import datetime


def do_pack():
    """Create a .tgz archive from the web_static folder"""
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
