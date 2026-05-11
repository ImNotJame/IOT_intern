from pwdlib import PasswordHash


def hash_password(password: str)-> str:
   hashed_password = PasswordHash.recommended()
   hashed_password = hashed_password.hash(password)
   return hashed_password


def verify_password(password: str, hashed_password: str)-> bool:
    return PasswordHash.recommended().verify(password, hashed_password)