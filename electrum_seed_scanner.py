#!/usr/bin/env python3

import io
import json
import os
import subprocess
import pyfiglet
from multiprocessing import Pool
import BIP39


def brute_force(wordlist):
    return (f"minor zone pool {word4} remain combine {word7} claw medal settle grace capable"
            for word4 in wordlist
            for word7 in wordlist)


def check_target(phrase):
    wallet_path = f"/home/user/.electrum/electrum_wallet/account_{phrase[0]}.json"
    result = subprocess.run(["electrum", "restore", "-w", wallet_path, phrase[1]],
                            capture_output=True, text=True)
    if result.returncode != 0:
        return None

    with io.open(wallet_path) as f:
        data = json.load(f)

    mnemonic = data["keystore"]["seed"]
    master_target = data["keystore"]["xpub"]

    if target == master_target:
        with io.open("/home/user/.electrum/ビットコイン.txt", "a") as f:
            f.write(f"{phrase[0] + 1} | {mnemonic}\n")
            f.write(f"{phrase[0] + 1} | {master_target}\n\n")
        print(f"found matching target in {wallet_path}")
        return True

    return None


def main():
    thread = 8
    with Pool(thread) as pool:
        seed_phrases = brute_force(BIP39.WORDLIST)
        results = pool.imap_unordered(check_target, enumerate(seed_phrases))

        for result in results:
            if result is not None:
                break


if __name__ == "__main__":
    result = pyfiglet.figlet_format("Scanning", font="slant")
    print(result)

    # target = "xpub661MyMwAqRbcEjyfaYRHPwe3xrXVBPQsH7fG4L46hDiJ2HRfaTZTFtm7igArBedocbuJkizWmyCuADHQfqz4VxGwqVbZV8t3pUfJ5i5EZs3"
    target = "zpub6nhhoBvkc6pNgU3JPwobardNLniafeTGnBkxrw8XLv3DeB24W2ycBD68dNciURmdUdqkbggGRCsSNCHg6UJCnYy4tA1GKMa1ZcRGK4Rpjth"
    mkdir = '/home/user/.electrum/electrum_wallet/'
    os.makedirs(mkdir, exist_ok=True)

    main()
