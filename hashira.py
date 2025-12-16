#!/usr/bin/env python3
"""
hashira - hash cracker
"""

import argparse
import hashlib
import multiprocessing as mp
import sys
from itertools import islice

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

HASH_FUNCS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
}

parser = argparse.ArgumentParser(description="hashira - fast multiprocessing hash cracker")
parser.add_argument("-H", "--hashes", required=True, help="Hash file")
parser.add_argument("-w", "--wordlist", required=True, help="Password wordlist")
parser.add_argument("--md5", action="store_true")
parser.add_argument("--sha1", action="store_true")
parser.add_argument("--sha256", action="store_true")
parser.add_argument("-o", "--output", help="Output file")
parser.add_argument("-j", "--jobs", type=int, default=mp.cpu_count(), help="Worker processes")
parser.add_argument("--chunk", type=int, default=20000, help="Words per chunk (increase for speed)")
parser.add_argument("--salt", help="Global salt (optional)")

args = parser.parse_args()

selected = [k for k in HASH_FUNCS if getattr(args, k)]
if len(selected) != 1:
    print(f"{RED}[-] Select exactly one hash type (--md5 / --sha1 / --sha256){RESET}")
    sys.exit(1)

hash_name = selected[0]
hash_func = HASH_FUNCS[hash_name]

# target_hash -> salt
hashes = {}
with open(args.hashes, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            h, s = line.split(':', 1)
            hashes[h.lower()] = s
        else:
            hashes[line.lower()] = args.salt

if not hashes:
    print(f"{RED}[-] No hashes loaded{RESET}")
    sys.exit(1)

hash_items = list(hashes.items())

def crack_chunk(words):
    found = []
    for word in words:
        data_word = word.rstrip('\n')
        if not data_word:
            continue
        for h, salt in hash_items:
            data = (data_word + (salt or '')).encode('latin-1')
            if hash_func(data).hexdigest() == h:
                found.append((h, data_word))
    return found

def chunks(fp, size):
    while True:
        block = list(islice(fp, size))
        if not block:
            break
        yield block

outfile = open(args.output, 'a') if args.output else None

remaining = set(hashes.keys())
checked = 0

with open(args.wordlist, 'r', encoding='latin-1', errors='ignore') as f, mp.Pool(args.jobs) as pool:
    for result in pool.imap_unordered(crack_chunk, chunks(f, args.chunk), chunksize=1):
        checked += args.chunk

        for h, word in result:
            if h in remaining:
                remaining.remove(h)
                msg = f"[+] FOUND ({hash_name}) {h} --> {YELLOW}{word}{RESET}"
                print(f"{msg}")
                if outfile:
                    outfile.write(msg + '\n')

        if checked % 1_000_000 == 0:
            print(f"{BLUE}[*] Checked ~{checked:,} passwords{RESET}")

        if not remaining:
            print(f"{YELLOW}[*] All hashes cracked. Stopping early.{RESET}")
            pool.terminate()
            break

if outfile:
    outfile.close()

print(f"{YELLOW}[*] Done. Checked ~{checked:,} passwords.{RESET}")
