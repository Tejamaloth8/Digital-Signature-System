import random
import hashlib

P = 2147483647  # large prime

class HeisenbergElement:
    def __init__(self, a, b, c):
        self.a = a % P
        self.b = b % P
        self.c = c % P

    def multiply(self, other):
        return HeisenbergElement(
            self.a + other.a,
            self.b + other.b,
            self.c + other.c + self.a * other.b
        )

    def power(self, n):
        result = HeisenbergElement(0, 0, 0)
        base = self
        while n > 0:
            if n % 2 == 1:
                result = result.multiply(base)
            base = base.multiply(base)
            n //= 2
        return result

    def serialize(self):
        return f"{self.a},{self.b},{self.c}".encode()

    @staticmethod
    def deserialize(data: str):
        a, b, c = map(int, data.split(","))
        return HeisenbergElement(a, b, c)


def hash_to_int(data: bytes):
    return int(hashlib.sha256(data).hexdigest(), 16) % P


def generate_keys():
    g = HeisenbergElement(1, 1, 0)
    private_key = random.randint(1, P - 1)
    public_key = g.power(private_key)
    return g, private_key, public_key


def sign(message: bytes, g, private_key):
    k = random.randint(1, P - 1)
    r = g.power(k)
    e = hash_to_int(r.serialize() + message)
    z = (k + private_key * e) % P
    return r, z


def verify(message: bytes, g, public_key, signature):
    r, z = signature
    e = hash_to_int(r.serialize() + message)
    left = g.power(z)
    right = r.multiply(public_key.power(e))
    return (
        left.a == right.a and
        left.b == right.b and
        left.c == right.c
    )
