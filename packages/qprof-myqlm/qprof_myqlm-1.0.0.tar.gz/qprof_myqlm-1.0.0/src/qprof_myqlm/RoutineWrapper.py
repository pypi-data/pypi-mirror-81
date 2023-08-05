# ======================================================================
# Copyright CERFACS (July 2019)
# Contributor: Adrien Suau (adrien.suau@cerfacs.fr)
#
# This software is governed by the CeCILL-B license under French law and
# abiding  by the  rules of  distribution of free software. You can use,
# modify  and/or  redistribute  the  software  under  the  terms  of the
# CeCILL-B license as circulated by CEA, CNRS and INRIA at the following
# URL "http://www.cecill.info".
#
# As a counterpart to the access to  the source code and rights to copy,
# modify and  redistribute granted  by the  license, users  are provided
# only with a limited warranty and  the software's author, the holder of
# the economic rights,  and the  successive licensors  have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using, modifying and/or  developing or reproducing  the
# software by the user in light of its specific status of free software,
# that  may mean  that it  is complicated  to manipulate,  and that also
# therefore  means that  it is reserved for  developers and  experienced
# professionals having in-depth  computer knowledge. Users are therefore
# encouraged  to load and  test  the software's  suitability as  regards
# their  requirements  in  conditions  enabling  the  security  of their
# systems  and/or  data to be  ensured and,  more generally,  to use and
# operate it in the same conditions as regards security.
#
# The fact that you  are presently reading this  means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
# ======================================================================

from ._interfaces import interfaces

from qat.lang.AQASM.gates import ParamGate, PredefGate, Gate


class RoutineWrapper(interfaces.RoutineWrapper):
    def __init__(self, gate: ParamGate, linking_set=None, _parent_controls: int = 0):
        super().__init__()
        self._gate = gate
        self._number_of_controlled_qubits = _parent_controls + (
            self._gate.nb_ctrls or 0
        )

        # Get the linking set in the appropriate format if not already.
        if linking_set is None:
            self._linking_set = dict()
        if isinstance(linking_set, list):
            self._linking_set = {gate.name: gate for gate in linking_set}
        else:
            self._linking_set = linking_set

        # If it is a boxed Gate, take the subgate
        if (
            isinstance(self._gate, Gate)
            and getattr(self._gate, "subgate", None) is not None
        ):
            self._gate = self._gate.subgate

        # If the gate is controlled, take the uncontrolled version.
        # Controls have already been registered in self._number_of_controlled_qubits.
        if self._gate.nb_ctrls is not None and self._gate.nb_ctrls > 0:
            self._gate = self._gate.subgate

        # Link the gate if needed
        if self._gate.name in self._linking_set:
            self._gate.abstract_gate.set_circuit_generator(
                self._linking_set[self._gate.name].circuit_generator
            )

        # If the gate is considered as primitive, it is already instantiated
        if self.is_base:
            self._instancied_gate = self._gate
        else:
            self._instancied_gate = self._gate.abstract_gate.get_circuit(
                *self._gate.parameters
            )

    @property
    def _instance(self):
        return self._instancied_gate

    def __iter__(self):
        return (
            RoutineWrapper(
                op.gate,
                linking_set=self._linking_set,
                _parent_controls=self._number_of_controlled_qubits,
            )
            for op in self._instance.op_list
        )

    @property
    def is_base(self):
        if isinstance(self._gate, PredefGate):
            return True
        elif isinstance(self._gate, ParamGate):
            return self._gate.abstract_gate.circuit_generator is None

    @property
    def name(self):
        subgate = self._gate.subgate
        base_name: str = self._gate.name if self._gate.name is not None else subgate.name
        if base_name.upper() == "X" and self._number_of_controlled_qubits > 0:
            base_name = "NOT"
        return (
            "C" * self._number_of_controlled_qubits
            + ("D" if self._gate.is_dag else "")
            + base_name
        )

    def __hash__(self):
        if self.is_base:
            return hash(self.name)
        return hash(
            (
                self._number_of_controlled_qubits,
                self._gate.parameters,
                id(self._gate.abstract_gate),
            )
        )

    def __eq__(self, other):
        if self.is_base and other.is_base:
            return self.name == other.name
        return (
            self._number_of_controlled_qubits == other._number_of_controlled_qubits
            and id(self._gate.abstract_gate) == id(other._gate.abstract_gate)
            and len(self._gate.parameters) == len(other._gate.parameters)
            and all(
                a == b for a, b in zip(self._gate.parameters, other._gate.parameters)
            )
        )

    @property
    def _is_controlled(self):
        return self._gate.nb_ctrls > 0
