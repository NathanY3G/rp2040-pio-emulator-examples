# SPDX-FileCopyrightText: Copyright 2024 Nathan Young
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
from typing import Dict

from pioemu import State
from pylibfst import lib as fst


@dataclass
class OutputVariable:
    name: str
    size_in_bits: int
    handle: int | None = None


def write_initial_values(writer, variables: Dict, initial_state: State):
    fst.fstWriterEmitTimeChange(writer, initial_state.clock)

    for name, variable in variables.items():
        fst.fstWriterEmitValueChange32(
            writer, variable.handle, variable.size_in_bits, getattr(initial_state, name)
        )


def write_changed_values(
    writer, variables: Dict, previous_state: State, current_state: State
):
    fst.fstWriterEmitTimeChange(writer, current_state.clock)

    for name, variable in variables.items():
        current_value = getattr(current_state, name)
        previous_value = getattr(previous_state, name)

        if current_value != previous_value:
            fst.fstWriterEmitValueChange32(
                writer, variable.handle, variable.size_in_bits, current_value
            )
