# SET PASSWORD
password="sar101"

# IMPORT FILES
import hashlib
import base64
from django.utils.crypto import (
    get_random_string, pbkdf2,
)
import random

#SET VALUES
algorithm = "pbkdf2_sha256"
iterations = 36000
length=12
allowed_chars='abcdefghijklmnopqrstuvwxyz''ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Salt
random = random.SystemRandom()
salt =''.join(random.choice(allowed_chars) for i in range(length))

# Hash
digest = hashlib.sha256
hash = pbkdf2(password, salt, iterations, digest=digest)
hash = base64.b64encode(hash).decode('ascii').strip()

# encoded_password
encoded_password="%s$%d$%s$%s" % (algorithm, iterations, salt, hash)
