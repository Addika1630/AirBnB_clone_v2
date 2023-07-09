#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""
import os
from fabric.api import local
from datetime import datetime

def do_pack():
    """Generate a .tgz archive from the contents of the web_static folder."""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # Create the versions folder if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Create the archive file name
    archive_name = "web_static_" + timestamp + ".tgz"

    try:
        # Compress the web_static folder into the archive
        local("tar -cvzf versions/{} web_static".format(archive_name))
        archive_path = "versions/{}".format(archive_name)
        print("web_static packed: {} -> {} Bytes".format(archive_path, os.path.getsize(archive_path)))
        return archive_path
    except Exception as e:
        print("Packaging failed: {}".format(e))
        return None
