#!/usr/bin/python3
"""Fabric script distributes an archive to web-servers"""

from fabric.api import put, env, local, run, runs_once
from datetime import datetime
import os

env.hosts = ["100.25.144.235", "3.85.136.215"]


@runs_once
def do_pack():
    """ generate a .tgz archive from all the files in web_static folder"""

    cur_time = datetime.now().strftime("%Y%m%dT%H%M%S")
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    archive_name = f"versions/web_static_{cur_time}.tgz"
    try:
        print(f"Packing web_static to {archive_name}")
        result = local(f"tar -czvf {archive_name} web_static/")
        if result.succeeded:
            print(f"versions/{archive_name}")
            archive_size = os.stat(archive_name).st_size
            print(f"web_static packed: {archive_name}->{archive_size} Bytes")
    except Exception:
        return None


def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """

    #  if empty argument passed
    if not os.path.exists(archive_path):
        return False

    basename = os.path.basename(archive_path)
    path = basename.replace('.tgz', '')
    path = '/data/web_static/releases/{}'.format(path)
    success = False
    try:
        #  upload archive to server
        put(archive_path, f'/tmp/{basename}')
        run('mkdir -p {}'.format(path))
        run('tar -xzf /tmp/{} -C {}'.format(basename, path))
        run(f'rm -rf /tmp/{basename}')
        run('mv {}/web_static/* {}'.format(path, path))
        run('rm -rf {}/web_static/'.format(path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(path))
        success = True
    except Exception:
        success = False
    return success

# def do_deploy(archive_path):
#     """function distributes the files in the archive to web-server"""
#     if not os.path.exists(archive_path):
#         return False
#     basename = os.path.basename(archive_path)
#     path = basename.replace(".tgx", "")
#     uncom_ar_path = f"/data/web_static/releases/{path}"
#     put(f"{archive_path}, /tmp/")
#     run(f"mkdir -p {uncom_ar_path}")
#     run(f"tar -xzvf /tmp/{basename} -C /{uncom_ar_path}")
#     run(f"rm -rf /tmp")
#     run(f"mv {uncom_ar_path}/web_static/* /{uncom_ar_path}")
#     run(f"rm -rf {archive_path}/web_static/")
#     run("rm -rf /data/web_static/current")
#     run(f"ln -s {uncom_ar_path} /data/web_static/current")
#     return True
