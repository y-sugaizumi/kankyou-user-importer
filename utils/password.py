import bcrypt


def hash_password(password: str) -> str:
    """Laravel互換のbcryptハッシュを生成"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
