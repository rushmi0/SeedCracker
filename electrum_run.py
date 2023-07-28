#!/usr/bin/env python3

import io
import json
import os
import subprocess
import pyfiglet
from multiprocessing import Pool
import BIP39

class ElectrumScanner:
    def __init__(self):
        self.target = None

    def brute_force(self, wordlist):
        return (f"minor zone pool {word4} remain combine {word7} claw medal settle grace capable"
                for word4 in wordlist
                for word7 in wordlist)

    def check_target(self, phrase):
        wallet_path = f"/home/username/.electrum/electrum_wallet/account_{phrase[0]}.json"
        result = subprocess.run(["electrum", "restore", "-w", wallet_path, phrase[1]],
                                capture_output=True, text=True)
        if result.returncode != 0:
            return None

        with io.open(wallet_path) as f:
            data = json.load(f)

        mnemonic = data["keystore"]["seed"]
        master_target = data["keystore"]["xpub"]

        if self.target == master_target:
            with io.open("/home/username/.electrum/myXpub.txt", "a") as f:
                f.write(f"{phrase[0] + 1} | {mnemonic}\n")
                f.write(f"{phrase[0] + 1} | {master_target}\n\n")
            print(f"found matching target in {wallet_path}")
            return True

        return None

    def main(self):
        thread = 5
        with Pool(thread) as pool:
            seed_phrases = self.brute_force(BIP39.WORDLIST)
            results = pool.imap_unordered(self.check_target, enumerate(seed_phrases))

            for result in results:
                if result is not None:
                    break

    def run(self):
        result = pyfiglet.figlet_format("Scanning", font="slant")
        print(result)

        self.target = "zpub6nhhoBvkc6pNgU3JPwobardNLniafeTGnBkxrw8XLv3DeB24W2ycBD68dNciURmdUdqkbggGRCsSNCHg6UJCnYy4tA1GKMa1ZcRGK4Rpjth"
        mkdir = '/home/username/.electrum/electrum_wallet/'
        os.makedirs(mkdir, exist_ok=True)

        self.main()

if __name__ == "__main__":
    scanner = ElectrumScanner()
    scanner.run()
