#!/usr/bin/env python3
'''
For AmazonLinux 2.0 - pre-requisites:
yum -y install python3 python3-devel
yum -y groupinstall "Development Tools"
'''

import logging
import argparse
import os
import struct
from Crypto.Cipher import AES
import glob


class EncryptMe(object):
    def __init__(self, args):
        self.args = args
        self.ENCRYPTION_KEY = self.args.key
        self.KEY_SIZE = 32  # bytes
        self.BLOCK_SIZE = 16  # bytes
        self.CHUNK_SIZE = 1 * 1024 * 1024 * 1024  # 1024Mb in bytes
        self.STREAM_BUFSIZE = self.CHUNK_SIZE * 4


    def encrypt_file(self, in_filename):
        key = self.ENCRYPTION_KEY
        chunksize = self.CHUNK_SIZE
        out_filename = in_filename + ".encrypted"
        iv = os.urandom(16)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            logging.info("encrypt_file: I am trying to encrypt " + in_filename)
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))

        logging.info(glob.glob(in_filename))
        logging.info(glob.glob(out_filename))


    def run(self):
            logging.info("Starting.")
            filename = self.args.file
            self.encrypt_file(filename)
            logging.info("Finished.")


if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            logging.FileHandler("./encrypt_me.log"),
            logging.StreamHandler() 
        ],
        format='%(asctime)s - %(message)s',
        level=logging.INFO
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The filename to encrypt.")
    parser.add_argument("--key", help="The encrpytion key.")
    args = parser.parse_args()

    EncryptMe(args).run()
