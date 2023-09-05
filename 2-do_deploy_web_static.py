#!/usr/bin/python3
"""Fabric script distributes an archive to web-servers"""

from fabric.api import put, env, local, run, runs_once
from datetime import datetime
import os

env.hosts = ["100.25.144.235", "3.85.136.215"]
env.user = "ubuntu"


# @runs_once
def do_pack():
    """ generate a .tgz archive from all the files in web_static folder"""

    cur_time = datetime.now().strftime("%Y%m%d%H%M%S")
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    archive_name = f"versions/web_static_{cur_time}.tgz"
    try:
        print("Packing web_static to {}".format(archive_name))
        result = local("tar -czvf {} web_static/".format(archive_name))
        if result.succeeded:
            print("versions/{}".format(archive_name))
            archive_size = os.stat(archive_name).st_size
            print("web_static packed: {}->{} Bytes".format(archive_name,archive_size))
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
        run("sudo mkdir -p {}".format(folder_path))
        run("sudo tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("sudo rm -rf /tmp/{}".format(file_name))
        run("sudo mv {}web_static/* {}".format(folder_path, folder_path))
        run("sudo rm -rf {}web_static".format(folder_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success
# def do_deploy(archive_path):
#     """Deploys the static files to the host servers.
#     Args:
#         archive_path (str): The path to the archived static files.
#     """

#     #  if empty argument passed
#     if not os.path.exists(archive_path):
#         return False

#     basename = os.path.basename(archive_path)
#     path = basename.replace('.tgz', '')
#     path = '/data/web_static/releases/{}'.format(path)
#     success = False
#     try:
#         #  upload archive to server
#         print("##### RUNNING do_deploy function ######\n")
#         print("putting archive in /tmp folder\n")
#         put(archive_path, f'/tmp/{basename}')
#         print("finish /tmp/\n")
#         print("making dir for archive without extension\n")
#         run('sudo mkdir -p {}'.format(path))
#         print("finish making dir without ext\n")
#         print("un-compress archive\n")
#         run('sudo tar -xzf /tmp/{} -C {}'.format(basename, path))
#         print("finish un-compress\n")
#         print("rm /tmp/ folder\n")
#         run(f'sudo rm -rf /tmp/{basename}\n')
#         print("finish removing /tmp\n")
#         print(f"mv {path}/web_static/* to {path}\n")
#         run('sudo mv {}/web_static/* {}'.format(path, path))
#         print("done moving\n")
#         print(f"remove {path}/web_static/\n")
#         run('sudo rm -rf {}/web_static/'.format(path))
#         print("done removing path\n")
#         print("removing /data/web_static/current\n ")
#         run('sudo rm -rf /data/web_static/current')
#         print("done removing /data/web_static/current\n")
#         print("doing linking\n")
#         run('sudo ln -s {} /data/web_static/current'.format(path))
#         print("linking done\n")
#         success = True
#     except Exception:
#         success = False
#     return success

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
