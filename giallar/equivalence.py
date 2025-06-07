from typing import Union

from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.converters import dag_to_circuit

from .core.impl.qcircuit import QCircuit
from .qiskit_wrapper.converter import certiq_circ_to_dag


def _to_qiskit_circuit(circ: Union[QuantumCircuit, QCircuit]) -> QuantumCircuit:
    """Convert a QuantumCircuit or :class:`QCircuit` to a QuantumCircuit."""
    if isinstance(circ, QuantumCircuit):
        return circ
    if isinstance(circ, QCircuit):
        dag = certiq_circ_to_dag(circ)
        return dag_to_circuit(dag)
    raise TypeError(f"Unsupported circuit type: {type(circ)}")


def circuits_equivalent(circ1: Union[QuantumCircuit, QCircuit],
                        circ2: Union[QuantumCircuit, QCircuit],
                        rtol: float | None = None,
                        atol: float | None = None) -> bool:
    """Return ``True`` if the two circuits are equivalent up to global phase."""
    qc1 = _to_qiskit_circuit(circ1).remove_final_measurements(inplace=False)
    qc2 = _to_qiskit_circuit(circ2).remove_final_measurements(inplace=False)

    op1 = Operator(qc1)
    op2 = Operator(qc2)
    return op1.equiv(op2, rtol=rtol, atol=atol)
