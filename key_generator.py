import random


def generate():
    key = ''
    abc = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    for i in range(20):
        random_letter = random.choice(abc)
        key += random_letter

    return key