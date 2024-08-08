import argparse
import json
import os
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
import jwt


def generate(keyfile, users):
    try:
        password = os.environ["KEY_PASSWORD"]
    except KeyError:
        password = None

    private_key: RSAPrivateKey = serialization.load_pem_private_key(
        keyfile.read(), password=password
    )

    tokens = {}
    for user in users:
        tokens[user] = jwt.encode(
            {"claimed_id": user},
            key=private_key,
            algorithm="RS256",
            headers={"kid": keyfile.name},
        )

    return tokens


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-c",
        "--count",
        type=int,
        default=argparse.SUPPRESS,
        help="Number of tokens to generate",
    )
    group.add_argument(
        "-u",
        "--users",
        type=str,
        nargs="+",
        default=argparse.SUPPRESS,
        help="Users to generate tokens for",
    )
    parser.add_argument(
        "key",
        type=argparse.FileType(mode="rb"),
        help="Path to an RS256 private key file",
    )

    argv = parser.parse_args()

    try:
        users = argv.users
    except AttributeError:
        users = [f"user{c}" for c in range(argv.count)]

    tokens = generate(argv.key, users)
    print(json.dumps(tokens, indent=2))


if __name__ == "__main__":
    main()
    sys.exit(0)
