# Copyright 2019-2020 The CertiQ authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np 
from sympy import I, Matrix, symbols, exp, cos, sin, zeros, eye
from sympy.physics.quantum import TensorProduct
from qiskit.converters import dag_to_circuit
from qiskit.quantum_info import Operator
# from qutip import QubitCircuit
from giallar.core.impl.error_handler import raise_error

# A class for verification using denotational semantics in CertiQ

class Simulator:

    def __init(self, qubit_state_num = 2): 
        self.qubit_state_num = qubit_state_num 

    @staticmethod
    def apply_circuit(circ):
        from giallar.qiskit_wrapper.converter import certiq_circ_to_dag
        dag = certiq_circ_to_dag(circ)
        qc = dag_to_circuit(dag)
        return Matrix(Operator(qc).data)

    @staticmethod
    def qutip_unitary(qcirc):

        qc = QubitCircuit(len(qcirc.qubits))
        for gate in qcirc.gate_list: 
            if gate.name == "H":
                tgt = circ.qbit2idx[gate.qubits[0]]-1
                qc.append("RX", targets=tgt, arg_value =np.pi/2)
                qc.append("RZ", targets=tgt, arg_value =np.pi/2)
                qc.append("RX", targets=tgt, arg_value =np.pi/2)

            if gate.name == "T":
                tgt = circ.qbit2idx[gate.qubits[0]]-1
                qc.append("RZ", targets=tgt, arg_value =np.pi/8)
            if gate.name == "Tdag":
                tgt = circ.qbit2idx[gate.qubits[0]]-1
                qc.append("RZ", targets=tgt, arg_value =-np.pi/8)

            if gate.name == "S":
                tgt = circ.qbit2idx[gate.qubits[0]]-1
                qc.append("RZ", targets=tgt, arg_value =np.pi/4)

            if gate.name == "X":
                tgt = circ.qbit2idx[gate.qubits[0]]-1
                qc.append("RX", targets=tgt, arg_value =np.pi)
            if gate.name == "Y":
                tgt = circ.qbit2idx[gate.qubits[0]]-1
                qc.append("RY", targets=tgt, arg_value =np.pi)
            if gate.name == "Z":
                tgt = circ.qbit2idx[gate.qubits[0]]-1
                qc.append("RZ", targets=tgt, arg_value =np.pi)
            if gate.name == "Rz":
                tgt = circ.qbit2idx[gate.qubits[0]]-1
                ang = gate.rot
                qc.append("RZ", targets=tgt, arg_value = ang)
            if gate.name == "Rx":
                tgt = circ.qbit2idx[gate.qubits[0]]-1
                ang = gate.rot
                qc.append("RX", targets=tgt, arg_value = ang)
            if gate.name == "CNOT":
                ctrl = circ.qbit2idx[gate.qubits[0]]-1
                tgt = circ.qbit2idx[gate.qubits[1]]-1
                qc.append("CNOT",controls=ctrl, targets=tgt)

        ulist = qc.propagators()
        u = gate_sequence_product(ulist)
        return u.full()

def _kron_list(args):
    ret = args[0]
    for item in args[1:]:
        ret = TensorProduct(ret, item)
    return ret

def GateMasterDef(name = '', para = None):
    
    if name.lower() in ['rz', 'rx', 'ry'] and para is None:
        raise_error("[Gate definition error] Rotation gate %s has no rotation angle provided." % name.lower())

    
    if name.lower() == 'h':
        return 1./np.sqrt(2) * Matrix([[1.0,  1.0],
                                       [1.0, -1.0]])

    if name.lower() == 'x':
        return Matrix([[0.0, 1.0],
                       [1.0, 0.0]])

    if name.lower() == 'y':
        return Matrix([[0.0, -1.0j],
                       [1.0j,0.0]])

    if name.lower() == 'cy':
        return Matrix([[1.0,0.0,0.0,0.0],
                       [0.0,1.0,0.0,0.0],
                       [0.0,0.0,0.0,-1.0j],
                       [0.0,0.0,1.0j,0.0]])

    if name.lower() == 'dcx':
        return Matrix([[1.0,0.0,0.0,0.0],
                       [0.0,0.0,0.0,1.0],
                       [0.0,1.0,0.0,0.0],
                       [0.0,0.0,1.0,0.0]])

    if name.lower() == 'cnot': 
        return Matrix([[1.0,0.0,0.0, 0.0],
                       [0.0,1.0,0.0, 0.0],
                       [0.0,0.0,0.0, 1.0], 
                       [0.0,0.0,1.0, 0.0]])

    if name.lower() == 'cz': 
        return Matrix([[1.0,0.0,0.0, 0.0], 
                       [0.0,1.0,0.0, 0.0], 
                       [0.0,0.0,1.0, 0.0], 
                       [0.0,0.0,0.0, -1.0]])

    if name.lower() == 'z':
        return Matrix([[1.0, 0.0],
                       [0.0,-1.0]])

    if name.lower() == 't':
        return Matrix([[1.0, 0.0], 
                       [0.0,exp(1j*np.pi/4.0)]])

    if name.lower() == 's':
        return Matrix([[1.0, 0.0],
                       [0.0,exp(1j*np.pi/2.0)]])

    if name.lower() in ['sx', 'sqrtx']:
        return Matrix([[0.5+0.5j, 0.5-0.5j],
                       [0.5-0.5j, 0.5+0.5j]])

    if name.lower() in ['sdag', 'sdg']:
        return Matrix([[1.0, 0.0],
                       [0.0,-exp(1j*np.pi/2.0)]])

    if name.lower() == 'tdag':
        return Matrix([[1.0, 0.0],
                       [0.0,-exp(1j*np.pi/4.0)]])

    if name.lower() == 'rz':
        return Matrix([[exp(-1j * para / 2), 0], 
                      [0, exp(1j * para / 2)]])

    if name.lower() == 'rx':
        return Matrix([[cos(para / 2), -1j * sin(para / 2)], 
                       [-1j * sin(para / 2), cos(para / 2)]])

    if name.lower() == 'ry':
        return Matrix([[cos(para / 2), - sin(para / 2)], 
                       [sin(para / 2), cos(para / 2)]])

    if name.lower() == 'u1':
        return Matrix([[exp(-1j * para / 2), 0], 
                      [0, exp(1j * para / 2)]])

    if name.lower() == 'u2':
        return 0.5 * np.sqrt(2) * Matrix([[1, -exp(1j * para[1])],
                                          [exp(1j * para[0]), exp(1j *(para[0] + para[1]))]])

    if name.lower() == 'u3':
        return Matrix([[cos(para[0] * 0.5), -exp(1j * para[2]) * sin(para[0] * 0.5)],
                       [exp(1j*para[1])*sin(para[0]*0.5), exp(1j*(para[1] + para[2])) * cos(para[0] * 0.5)]])


    if name.lower() == 'p0':
        return Matrix([[1.0, 0.0], 
                       [0.0,0.0]]) 

    if name.lower() == 'p1':
        return Matrix([[0.0, 0.0],
                       [0.0,1.0]])

    if name.lower() == 'p01':
        return Matrix([[0.0, 0.0],
                       [1.0,0.0]])

    if name.lower() == 'p10':
        return Matrix([[0.0, 1.0],
                       [0.0,0.0]])

    if name.lower() in ['id', 'barrier', 'measure']:
        return Matrix([[1.0, 0.0],
                       [0.0, 1.0]])

    if name.lower() == 'iswap':
        return Matrix([[1.0,0.0,0.0, 0.0], 
                       [0.0,0.,1.0j, 0.0], 
                       [0.0,1.0j,0., 0.0], 
                       [0.0,0.0,0.0, 1.0]])

    if name.lower() == 'ms':
        return Matrix([[1.0,0.0,0.0, -1j], 
                       [0.0,1.0,-1j, 0.0], 
                       [0.0,-1j,1.0, 0.0], 
                       [-1j,0.0,0.0, 1.0]])

    return None

def flip_matrix(mat):
    # TODO
    return mat

gate_info = { 
              'swap': {'id': 0, 'argn': 2, 'type': 0},
              'cnot': {'id': 1, 'argn': 2, 'type': 1},
              'cy': {'id': 2, 'argn': 2, 'type': 2},
              'cz': {'id': 3, 'argn': 2, 'type': 3},
              'dcx': {'id': 24, 'argn': 2, 'type': 2},
              'h': {'id': 4, 'argn': 1, 'type': 4},
              'y': {'id': 5, 'argn': 1, 'type': 5},
              'z': {'id': 6, 'argn': 1, 'type': 6},
              'u1': {'id': 7, 'argn': 1, 'type': 6},
              'rz': {'id': 8, 'argn': 1, 'type': 6},
              't': {'id': 9, 'argn': 1, 'type': 6},
              's': {'id': 10, 'argn': 1, 'type': 6},
              'sdg': {'id': 22, 'argn': 1, 'type': 6},
              'sx': {'id': 23, 'argn': 1, 'type': 7},
              'rx': {'id': 11, 'argn': 1, 'type': 7},
              'x': {'id': 12, 'argn': 1, 'type': 7},
              'barrier': {'id': 13, 'argn': 1, 'type':8},
              'iswap': {'id': 14, 'argn': 2, 'type': 9},
              'ms': {'id': 15, 'argn': 2, 'type': 10},
              'measure': {'id':16, 'argn': 1, 'type': 11},
              'reset': {'id':17, 'argn': 1, 'type': 12},
              'ry': {'id':18, 'argn': 1, 'type': 13},
              'u2': {'id':19, 'argn': 1, 'type': 14},
              'u3': {'id':20, 'argn': 1, 'type': 15},
              'id': {'id':21, 'argn': 1, 'type':16}
            }
