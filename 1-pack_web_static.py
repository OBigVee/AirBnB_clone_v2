#!/usr/bin/env python3
"""fabric script generates a .tgz archive from the contents of web_static folder"""

from datetime import datetime
from fabric import local


def do_pack():
    """ generate a .tgz archive from all the files in web_static folder"""
    # run("mkdir /web_static")
    try:    
        time = datetime.now().strftime("%Y%m%dT%H%M%S")
        
        local("mkdir -p versions")

        archive_name = f"web_static_{time}.tgz"

        local(f"tar -czvf versions/{archive_name} web_static")
        
        return f"versions/{archive_name}"
    
    except Exception:
        return None