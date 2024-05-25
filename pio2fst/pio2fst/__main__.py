# SPDX-FileCopyrightText: Copyright 2024 Nathan Young
#
# SPDX-License-Identifier: Apache-2.0
import click
from adafruit_pioasm import assemble
from pioemu import State, clock_cycles_reached, emulate
from pylibfst import lib as fst

from pio2fst import OutputVariable, write_changed_values, write_initial_values

# Specify which of the emulator's fields are to be output to the trace file.
output_variables = {
    "clock": OutputVariable("CLK", 32),
    "program_counter": OutputVariable("PC", 5),
    "pin_values": OutputVariable("GPIO", 32),
    "x_register": OutputVariable("X", 32),
    "y_register": OutputVariable("Y", 32),
}


@click.command()
@click.option(
    "--input",
    required=True,
    type=str,
    help="Name of file to load PIO program source from",
)
@click.option(
    "--output",
    default="out.fst",
    type=str,
    help="Name to use for the generated FST file",
)
@click.option("--samples", required=True, type=int, help="Number of samples to acquire")
def run(input: str, output: str, samples: int):
    with open(input, mode="rt", encoding="UTF-8") as file:
        program = assemble(file.read())

    writer = fst.fstWriterCreate(output.encode("UTF-8"), 0)
    fst.fstWriterSetPackType(writer, fst.FST_WR_PT_LZ4)
    fst.fstWriterSetComment(
        writer, "Example output from rp2040-pio-emulator".encode("UTF-8")
    )

    for variable in output_variables.values():
        variable.handle = fst.fstWriterCreateVar(
            writer,
            fst.FST_VT_SV_LOGIC,
            fst.FST_VD_OUTPUT,
            variable.size_in_bits,
            variable.name.encode("UTF-8"),
            0,
        )

    initial_state = State()

    write_initial_values(writer, output_variables, initial_state)

    for previous_state, current_state in emulate(
        program,
        initial_state=initial_state,
        stop_when=clock_cycles_reached(samples),
    ):
        write_changed_values(writer, output_variables, previous_state, current_state)

    fst.fstWriterClose(writer)


if __name__ == "__main__":
    run()
