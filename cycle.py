#!/usr/bin/env python
import random

class Perm(dict):
    def __init__(self, d):
        self.update(d)
        self.n = len(self)

        # Verify that it is really a permutation
        assert set(self.iterkeys()) == set(self.itervalues())
        assert set(self.iterkeys()) == set(xrange(1, self.n + 1))

    def __setitem__(self):
        raise AttributeError("Permutations are immutable")

    def __repr__(self):
        terms = ['%d: %d' % (i, self[i]) for i in xrange(1, self.n + 1)]
        return 'Perm({%s})' % ', '.join(terms)

    def __mul__(a, b):
        """ Multiply (compose) permutations """
        return Perm({i: a[b[i]] for i in b})

    def __eq__(a, b):
        """ Compare two permutations """
        return a.n == b.n and all(a[i] == b[i] for i in xrange(1, a.n + 1))

    def __pow__(self, exp):
        if exp == 0:
            return Perm.ident(self.n)
        elif exp == 1:
            return self
        elif exp % 2 == 1:
            return self * self**(exp - 1)
        else:
            half = self**(exp / 2)
            return half * half

    def dumb_pow(self, exp):
        perm = Perm.ident(self.n)
        for i in xrange(exp):
            perm = perm * self
        return perm

    def __ne__(a, b):
        return not (a == b)

    def cycles(self):
        """Return the cycles in this permutation"""
        cycles = set()
        needed = set(self.iterkeys())
        while needed:
            key = needed.pop()
            cycle = [key]
            while self[key] != cycle[0]:
                key = self[key]
                cycle.append(key)
                needed.remove(key)
            cycles.add(tuple(cycle))
        return cycles

    @staticmethod
    def ident(n):
        """ Get the identity permutation for 1...n """
        return Perm({i: i for i in xrange(1, n+1)})

    @staticmethod
    def cycle(n, cyc):
        """ Create a permutation with a single cycle.
            Example:  cycle(5, [1, 4, 2, 5])
        """
        partial = {cyc[j]: cyc[(j+1) % len(cyc)] for j in xrange(len(cyc))}
        return Perm({i: partial.get(i, i) for i in xrange(1, n+1)})

    @staticmethod
    def random(n):
        """Generate a random permutation of 1...n"""
        nlist = range(1, n + 1)
        random.shuffle(nlist)
        return Perm({i + 1: v for i, v in enumerate(nlist)})

# print Perm.cycle(5, [1, 4, 2, 5])
# print Perm.ident(3)
a = Perm.cycle(4, [1,2])
b = Perm.cycle(4, [3,4])
# print a
# print b
# print a*b
# print b*a
# print a*b == b*a
# print (a*b).cycles()
for n in xrange(100):
    perm = Perm.random(100)
    print "perm is ", perm
    assert perm**n == perm.dumb_pow(n)


