#!/usr/bin/env python3

import uuid
from shutil import copy
import subprocess
import os
import sys

CHALL_ORIGIN_FILE = "./changebyone2"
CHALL_OUT_FILE    = "/tmp/" + str(uuid.uuid4())

def run(offset=None, value=None):
    copy(CHALL_ORIGIN_FILE, CHALL_OUT_FILE)
    if offset is not None and value is not None:
        with open(CHALL_OUT_FILE, 'r+b') as f:
            f.seek(offset)
            f.write(bytes([value % 256]))

    sys.stdout.flush()

    try:
        proc = subprocess.Popen([CHALL_OUT_FILE], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    except Exception as e:
        os.remove(CHALL_OUT_FILE)
        print("Error when trying to execute : %s" % e)
    else:
        os.remove(CHALL_OUT_FILE)
        proc.wait()

def get_int(comment="", default=0):
    answer = input(comment)
    try:
        answer_int = int(answer, 0)
    except ValueError:
        return default
    else:
        return answer_int

if __name__ == "__main__":
    print("Hi,\n\n"
          "Before starting to exploit my unbreakable program, I give you an opportunity.\n"
          "You can change one byte of my binary.")

    answer = input("Do you use this opportunity [Y/n] : ")
    if "n" in answer or "N" in answer:
        print("Ok, It's your choice.\n\n"
              "Have fun !!!")
        run()
    else:
        offset = get_int("offset : ")
        value  = get_int("value : ")
        print("Ok, Thank's.\n\n"
              "Enjoy your chall !!!")
        run(offset, value)
