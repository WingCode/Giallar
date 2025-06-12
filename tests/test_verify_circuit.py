import time
from qiskit import QuantumCircuit
from qiskit.circuit.random import random_clifford_circuit
# from mqt import qcec
from giallar.verify_circuit import verify_circuit
import ucc

# --- Step 1: Generate a random Clifford circuit ---
def generate_random_clifford_circuit(num_qubits, seed=12345):
    gates = ["cx", "cz", "cy", "swap", "x", "y", "z", "s", "sdg", "h"]
    qc = random_clifford_circuit(
        num_qubits,
        gates=gates,
        num_gates=10 * num_qubits * num_qubits,
        seed=seed,
    )
    return qc

def test_giallar_compile():
    # --- Step 2: Generate and compile the circuit ---
    num_qubits = 50
    raw_n100_circuit = generate_random_clifford_circuit(num_qubits)
    compiled_circuit = ucc.compile(raw_n100_circuit)

    # --- Step 3: Verify raw vs raw ---
    # start_time_raw = time.perf_counter()
    # res_raw = qcec.verify(raw_n100_circuit, raw_n100_circuit)
    # end_time_raw = time.perf_counter()
    # duration_raw = end_time_raw - start_time_raw 
    # min_raw, sec_raw = divmod(duration_raw, 60)
    # print(f"Verification (raw vs raw): {res_raw}")
    # print(f"Time taken: {int(min_raw)} min {sec_raw:.2f} sec")

    # --- Step 4: Verify raw vs compiled ---
    start_time_comp = time.perf_counter()
    res_comp = verify_circuit(raw_n100_circuit, compiled_circuit) #  Verification (raw vs compiled): True Time taken: 0 min 46.96 sec, 10qubits
    # res_comp = qcec.verify(raw_n100_circuit, compiled_circuit)  # More than 5 minutes. 10 qubits
    print(res_comp)
    end_time_comp = time.perf_counter()
    duration_comp = end_time_comp - start_time_comp
    min_comp, sec_comp = divmod(duration_comp, 60)
    print(f"Verification (raw vs compiled): {res_comp}")
    print(f"Time taken: {int(min_comp)} min {sec_comp:.2f} sec")


def test_equivalent_circuits():
    qc1 = QuantumCircuit(1)
    qc1.h(0)
    qc1.x(0)

    qc2 = QuantumCircuit(1)
    qc2.h(0)
    qc2.x(0) 

    assert verify_circuit(qc1, qc2)

def test_inequivalent_circuits():
    qc1 = QuantumCircuit(1)
    qc1.h(0)
    qc1.x(0)

    qc2 = QuantumCircuit(1)
    qc2.x(0)
    qc2.h(0)

    assert not verify_circuit(qc1, qc2)