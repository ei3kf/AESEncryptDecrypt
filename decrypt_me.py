#!/usr/bin/env python3
'''
For AmazonLinux 2.0 - pre-requisites:
yum -y install python3 python3-devel
yum -y groupinstall "Development Tools"
'''

import logging
import argparse
import struct
from Crypto.Cipher import AES
import glob


class DecryptMe(object):
    def __init__(self, args):
        self.args = args
        self.ENCRYPTION_KEY = self.args.key
        self.KEY_SIZE = 32  # bytes
        self.BLOCK_SIZE = 16  # bytes
        self.CHUNK_SIZE = 1 * 1024 * 1024 * 1024  # 1024Mb in bytes
        self.STREAM_BUFSIZE = self.CHUNK_SIZE * 4


    def decrypt_file(self, in_filename):
        key = self.ENCRYPTION_KEY
        chunksize = self.CHUNK_SIZE
        out_filename = in_filename.split(".encrypted")[0] ## remove .encrypted from the filename.

        with open(in_filename, 'rb') as infile:
            logging.info("decrypt_file: I am trying to decrypt " + in_filename)
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)

        logging.info(glob.glob(in_filename))
        logging.info(glob.glob(out_filename))


    def run(self):
            logging.info("Starting.")
            filename = self.args.file
            self.decrypt_file(filename)
            logging.info("Finished.")


if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            logging.FileHandler("./decrypt_me.log"),
            logging.StreamHandler() 
        ],
        format='%(asctime)s - %(message)s',
        level=logging.INFO
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The filename to decrypt.")
    parser.add_argument("--key", help="The encrpytion key.")
    args = parser.parse_args()

    DecryptMe(args).run()

   
