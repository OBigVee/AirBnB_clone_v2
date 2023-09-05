#!/usr/bin/python3
"""Fabric script distributes an archive to web-servers"""

from fabric.api import put, env, local, run
from datetime import datetime
import os

env.hosts = ["100.25.144.235" ,"3.85.136.215"]
env.user = "ubuntu"
def do_pack():
    """ generate a .tgz archive from all the files in web_static folder"""

    time = datetime.now().strftime("%Y%m%dT%H%M%S")

    local("mkdir -p versions")

    archive_name = f"web_static_{time}.tgz"

    result = local(f"tar -czvf versions/{archive_name} web_static/")
    if result.succeeded:
        return f"versions/{archive_name}"
    else:
        return None
    
def do_deploy(archive_path):
    """function distributes the files in the archive to web-server"""
    if not os.path.exists(archive_path):
        return False
    
    basename = os.path.basename(archive_path)
    path = basename.replace(".tgx", "")

    uncom_ar_path = f"/data/web_static/releases/{path}"
        
    put(f"{archive_path}, /tmp/")
    run(f"mkdir -p {uncom_ar_path}")
    run(f"tar -xzvf /tmp/{basename} -C /{uncom_ar_path}")
    run(f"rm -rf /tmp")
    run(f"mv {uncom_ar_path}/web_static/* /{uncom_ar_path}")
    run(f"rm -rf {archive_path}/web_static/")
    run("rm -rf /data/web_static/current")
    run(f"ln -s {uncom_ar_path} /data/web_static/current")
    return True
