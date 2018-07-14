import shutil

from .smart_open_lib import *

DEFAULT_CHUNKSIZE = 16*1024*1024 # 16mb

def copy_file(src, dest, close_src=True, close_dest=True, make_path=False):
    """
    Copies file from src to dest. Supports s3 and webhdfs (does not include kerberos support)

    If src does not exist, a FileNotFoundError is raised.

    :param src: file-like object or path
    :param dest: file-like object or path
    :param close_src: boolean (optional). if True, src file is closed after use.
    :param close_dest: boolean (optional). if  True, dest file is closed after use.
    :param make_path: str (optional, default False). if True, destination parent directories are created if missing. Only if path is local
    """
    logging.info("Copy file from {} to {}".format(src, dest))
    if make_path:
        dir_path, _ = os.path.split(dest)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

    in_file = smart_open(src, 'rb')
    out_file = smart_open(dest, 'wb')

    try:
        shutil.copyfileobj(in_file, out_file, DEFAULT_CHUNKSIZE)
    except NotImplementedError as e:
        logging.info("Error encountered copying file. Falling back to looping over input file. {}".format(e))
        for line in in_file:
            out_file.write(line)

    try:
        out_file.flush()
    except Exception as e:
        logging.info("Unable to flush out_file")

    if in_file and not in_file.closed and close_src:
        in_file.close()

    if out_file and not out_file.closed and close_dest:
        out_file.close()
