from sys import stdin
from sys import setrecursionlimit
from math import *
from random import randint
from collections import Counter
from fractions import Fraction
def inputline(type, split=False):
	if split:
		return list(map(type, stdin.readline().strip().split()))
	else:
		return type(stdin.readline().strip())

class object:
	def __init__(self, mass: int, velocity: Fraction):
		self.m = mass
		self.v = velocity

def collision(object1: object, object2 : object):
	v1 = object1.v
	v2 = object2.v
	object1.v = Fraction(
		v1 * (object1.m - object2.m) + v2 * (2 * object2.m),
		object1.m + object2.m
	)
	object2.v = Fraction(
		v1 * (2 * object1.m) - v2 * (object1.m - object2.m),
		object1.m + object2.m
	)

if __name__ == '__main__':
	n = inputline(int)

	object1 = object(1, Fraction(0))
	object2 = object(n**2, Fraction(-1))

	c = 0
	while True:
		if 0 <= object1.v <= object2.v:
			break

		if object1.v < 0 and object1.v <= object2.v:
			object1.v *= -1
		else:
			collision(object1, object2)
		c += 1

	print(c)