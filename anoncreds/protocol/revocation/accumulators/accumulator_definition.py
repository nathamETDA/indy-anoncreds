from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, pair

from anoncreds.protocol.revocation.accumulators.types import RevocationPublicKey, RevocationSecretKey, \
    Accumulator, AccumulatorPublicKey, AccumulatorSecretKey


class AccumulatorDefinition:
    def __init__(self, group: PairingGroup = None):
        self.group = group if group else PairingGroup('SS1024')  # super singular curve, 1024 bits

    def genRevocationKeys(self):
        h = self.group.random(G1)  # random element of the group G
        h0 = self.group.random(G1)
        h1 = self.group.random(G1)
        h2 = self.group.random(G1)
        g = self.group.random(G1)
        htilde = self.group.random(G1)
        u = self.group.random(G1)

        qr = self.group.order()  # order q_R of the group

        x = self.group.random(ZR)  # random(qr)
        sk = self.group.random(ZR)  # random(qr)

        pk = g ** sk
        y = h ** x

        return (RevocationPublicKey(qr, g, h, h0, h1, h2, htilde, u, pk, y, x), RevocationSecretKey(x, sk))

    def issueAccumulator(self, iA, pk: RevocationPublicKey, L):
        gamma = self.group.random(ZR)

        gi = {}
        gCount = 2 * L
        for i in range(gCount):
            if i != L + 1:
                gi[i] = pk.g ** (gamma ** i)
        z = pair(pk.g, pk.g) ** (gamma ** (L + 1))

        acc = 1
        V = set()

        accPK = AccumulatorPublicKey(z)
        accSK = AccumulatorSecretKey(gamma)
        return (Accumulator(iA, acc, V, accPK, L), gi, accSK)
