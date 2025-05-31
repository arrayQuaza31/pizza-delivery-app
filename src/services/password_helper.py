from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

def generate_password_hash(pwd: str) -> str:
    pwd_hash = PWD_CONTEXT.hash(pwd)
    return pwd_hash

def verify_password(pwd: str, hash: str) -> bool:
    return PWD_CONTEXT.verify(pwd, hash)