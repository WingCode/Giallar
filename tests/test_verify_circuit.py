from qiskit import QuantumCircuit
from giallar.verify_circuit import verify_circuit

def test_equivalent_circuits():
    qc1 = QuantumCircuit(1)
    qc1.h(0)
    qc1.x(0)

    qc2 = QuantumCircuit(1)
    qc2.h(0)
    qc2.x(0)

    assertTrue(verify_circuit(qc1, qc2))

def test_inequivalent_circuits():
    qc1 = QuantumCircuit(1)
    qc1.h(0)
    qc1.x(0)

    qc2 = QuantumCircuit(1)
    qc2.x(0)
    qc2.h(0)

    self.assertFalse(verify_circuit(qc1, qc2))
