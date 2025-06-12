from qiskit.converters import circuit_to_dag
from qiskit.circuit import QuantumCircuit

from giallar.qiskit_wrapper.converter import dag_to_certiq_circ
from giallar.gate_info import Simulator
import numpy as np


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
    return _equal_up_to_global_phase(mat_a, mat_b)


def _equal_up_to_global_phase(mat_a, mat_b):
    """Return True if two matrices are equal up to global phase."""
    if mat_a.shape != mat_b.shape:
        return False

    arr_a = np.array(mat_a.tolist(), dtype=complex)
    arr_b = np.array(mat_b.tolist(), dtype=complex)

    # find first non-zero element to compute phase
    idx = None
    for i, (a, b) in enumerate(zip(arr_a.flatten(), arr_b.flatten())):
        if abs(b) > 1e-12:
            idx = i
            break
    if idx is None:
        return True

    phase = arr_a.flatten()[idx] / arr_b.flatten()[idx]
    return np.allclose(arr_a, phase * arr_b, atol=1e-8)
