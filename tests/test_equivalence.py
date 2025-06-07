import unittest
from qiskit import QuantumCircuit
from giallar import circuits_equivalent

class EquivalenceTest(unittest.TestCase):
    def test_identity_equivalence(self):
        qc1 = QuantumCircuit(1)
        qc1.h(0)
        qc1.h(0)

        qc2 = QuantumCircuit(1)

        self.assertTrue(circuits_equivalent(qc1, qc2))

    def test_not_equivalent(self):
        qc1 = QuantumCircuit(1)
        qc1.x(0)
        qc2 = QuantumCircuit(1)
        qc2.h(0)
        self.assertFalse(circuits_equivalent(qc1, qc2))

if __name__ == '__main__':
    unittest.main()
