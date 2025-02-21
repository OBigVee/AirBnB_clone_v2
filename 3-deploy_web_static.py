#!/usr/bin/python3
"""script creates and distributes an archive to
web servers, using the function deploy"""

from fabric.api import put, env, local, run
from datetime import datetime
import os

env.hosts = ["100.25.144.235", "3.85.136.215"]
env.user = "ubuntu"


def do_pack():
    """ generate a .tgz archive from all the files in web_static folder"""

    cur_time = datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    archive_name = "versions/web_static_{}.tgz".format(cur_time)
    try:
        print("Packing web_static to {}".format(archive_name))
        result = local("tar -czvf {} web_static/".format(archive_name))
        if result.succeeded:
            print("versions/{}".format(archive_name))
            archive_size = os.stat(archive_name).st_size
            print("web_static packed: {}->{} Bytes".format(archive_name,
                                                           archive_size))
    except Exception:
        return None


def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """function calls do_pack and do_deploy functions"""
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
