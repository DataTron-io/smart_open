from tempfile import NamedTemporaryFile

import time

from smart_open import copy_file

mb = 1024*1024
gb = 1024 * mb

def BenchmarkCopyFile(size):
    with NamedTemporaryFile() as f:
        f.seek(size)
        f.write(b'0')
        f.flush()

        start = time.time()
        copy_file(f.name, 's3://staging-shivastg/test/{}'.format(f.name.split('/')[-1]))
        end = time.time()
        print("file size: {}mb time taken: {} s".format(size/mb, end-start))

if __name__ == '__main__':
    for size in [1*mb, 10*mb, 100*mb]:
        BenchmarkCopyFile(size)

# On local machine (MacBook Pro)
# file size: 1.0mb time taken: 6.426445722579956 s
# file size: 10.0mb time taken: 8.901501893997192 s
# file size: 100.0mb time taken: 42.31656002998352 s
# file size: 1024.0mb time taken: 395.94028306007385 s