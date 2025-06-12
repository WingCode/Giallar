from qiskit.converters import circuit_to_dag
from qiskit.circuit import QuantumCircuit

from giallar.qiskit_wrapper.converter import dag_to_certiq_circ
from giallar.gate_info import Simulator


def verify_circuit(circ_a: QuantumCircuit, circ_b: QuantumCircuit) -> bool:
    """Verify logical equivalence between two Qiskit circuits using CertiQ logic.

    Parameters
    ----------
    circ_a : QuantumCircuit
        First circuit to compare.
    circ_b : QuantumCircuit
        Second circuit to compare.

    Returns
    -------
    bool
        ``True`` if the circuits are equivalent, otherwise ``False``.
    """
    dag_a = circuit_to_dag(circ_a)
    dag_b = circuit_to_dag(circ_b)

    impl_a = dag_to_certiq_circ(dag_a)
    impl_b = dag_to_certiq_circ(dag_b)

    # Use CertiQ's simulator to compute the matrices and compare them
    mat_a = Simulator.apply_circuit(impl_a)
    mat_b = Simulator.apply_circuit(impl_b)

    return mat_a == mat_b
