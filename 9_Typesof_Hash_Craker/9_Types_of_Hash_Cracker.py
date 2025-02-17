#!/usr/bin/env python3

import hashlib
import itertools
import multiprocessing
import os
import string
import threading
import time
import logging

class Cracker(object):
    # ... (Your existing code for character sets)

    def __init__(self, hash_type, hash, charset, progress_interval):
        self.__charset = charset
        self.__curr_iter = 0
        self.__prev_iter = 0
        self.__curr_val = ""
        self.__progress_interval = progress_interval
        self.__hash_type = hash_type
        self.__hash = hash
        self.__hashers = {}
        self.__init_logger()

    def __init_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def __init_hasher(self):
        hashlib_type = self.__hash_type if self.__hash_type != "ntlm" else "md4"
        self.__hashers[self.__hash_type] = hashlib.new(hashlib_type)

    def __encode_utf8(self, data):
        return data.encode("utf-8")

    def __encode_utf16le(self, data):
        return data.encode("utf-16le")

    @staticmethod
    def __search_space(charset, maxlength):
        return (
            ''.join(candidate) for candidate in
            itertools.chain.from_iterable(
                itertools.product(charset, repeat=i) for i in
                range(1, maxlength + 1)
            )
        )

    def __attack(self, q, max_length):
        self.__init_hasher()
        self.start_reporting_progress()
        hash_fn = self.__encode_utf8 if self.__hash_type != "ntlm" else self.__encode_utf16le
        for value in self.__search_space(self.__charset, max_length):
            hasher = self.__hashers[self.__hash_type].copy()
            self.__curr_iter += 1
            self.__curr_val = value
            hasher.update(hash_fn(value))
            if self.__hash == hasher.hexdigest():
                q.put("FOUND")
                q.put("{}Match found! Password is {}{}".format(
                    os.linesep, value, os.linesep))
                self.stop_reporting_progress()
                return

        q.put("NOT FOUND")
        self.stop_reporting_progress()

    @staticmethod
    def work(work_q, done_q, max_length):
        obj = work_q.get()
        obj.__attack(done_q, max_length)

    def start_reporting_progress(self):
        self.__progress_timer = threading.Timer(
            self.__progress_interval, self.start_reporting_progress)
        self.__progress_timer.start()
        self.logger.info(f"Character set: {self.__charset}, iteration: {self.__curr_iter}, trying: {self.__curr_val}, hashes/sec: {self.__curr_iter - self.__prev_iter}")
        self.__prev_iter = self.__curr_iter

    def stop_reporting_progress(self):
        self.__progress_timer.cancel()
        self.logger.info(f"Finished character set {self.__charset} after {self.__curr_iter} iterations")

if __name__ == "__main__":
    character_sets = {
        # ... (Your existing character sets)
    }

    hashes = {
        # ... (Your existing hashes)
    }

    prompt = "Specify the character set to use:{}{}".format(
        os.linesep, os.linesep)
    for key, value in sorted(character_sets.items()):
        prompt += "{}. {}{}".format(key, ''.join(value), os.linesep)

    while True:
        try:
            charset = input(prompt).zfill(2)
            selected_charset = character_sets[charset]
        except KeyError:
            print("{}Please select a valid character set{}".format(
                os.linesep, os.linesep))
            continue
        else:
            break

    prompt = "{}Specify the maximum possible length of the password: ".format(
        os.linesep)

    while True:
        try:
            password_length = int(input(prompt))
        except ValueError:
            print("{}Password length must be an integer".format(os.linesep))
            continue
        else:
            break

    prompt = "{}Specify the hash's type:{}".format(os.linesep, os.linesep)
    for key, value in sorted(hashes.items()):
        prompt += "{}. {}{}".format(key, value, os.linesep)

    while True:
        try:
            hash_type = hashes[input(prompt).zfill(2)]
        except KeyError:
            print("{}Please select a supported hash type".format(os.linesep))
            continue
        else:
            break

    prompt = "{}Specify the hash to be attacked: ".format(os.linesep)

    while True:
        try:
            user_hash = input(prompt)
        except ValueError:
            print("{}Something is wrong with the format of the hash. Please enter a valid hash".format(
                os.linesep))
            continue
