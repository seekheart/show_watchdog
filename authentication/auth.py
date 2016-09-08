import hashlib
import random
import string

def sha256_hash(string):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def random_fixed_string(size=32):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(size))

if __name__=="__main__":
    print(sha256_hash("ayylemon"))