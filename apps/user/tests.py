import random
from django.test import TestCase

# Create your tests here.
def getRandCode():
    data = "0123456789"
    l = []
    for i in range(4):
        l.append(random.choice(data))
    return "".join(l)


print(getRandCode())