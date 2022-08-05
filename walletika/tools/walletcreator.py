from web3 import Web3
import pyotp
import typing
import base64
import hashlib
import aescrypto


def otp_hash(username: str, password: str, password_recovery: str) -> str:
    pass


def access(
        username: str, password: str, password_recovery: typing.Union[str, bytes], otp_code: str
) -> typing.Tuple[str, str, bytes]:
    pass


__all__ = ['otp_hash', 'access']
