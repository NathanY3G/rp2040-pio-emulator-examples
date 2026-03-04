# Example: FIFO Loopback

This example demonstrates the full TX/RX FIFO data path by emulating a simple
PIO loopback program.

## PIO Program

```pio
pull block      ; Pull value from TX FIFO into OSR
out pins, 32    ; Write OSR to pins (all 32 bits)
in pins, 32     ; Read pins into ISR (reads back what we just wrote)
push block      ; Push ISR contents to RX FIFO
```

Data flows through the state machine in one direction:

```
TX FIFO -> OSR -> pins -> ISR -> RX FIFO
```

## What It Shows

- Pre-loading the **TX FIFO** (`transmit_fifo`) in the initial `State` to
  simulate CPU writes
- Reading back results from the **RX FIFO** (`receive_fifo`) after emulation
- Detecting a **stall** when `pull block` finds the TX FIFO empty
- Tracing state machine internals (OSR, ISR, pin values) cycle by cycle

## Running

```bash
python fifo_loopback.py
```

Example output:

```
Emulating PIO loopback: TX FIFO -> pins -> RX FIFO
TX FIFO starts with: ['0xdeadbeef', '0xcafebabe', '0x12345678']

clock  1  PC=0  pull block      OSR <- 0xdeadbeef
clock  2  PC=1  out pins, 32    pins <- 0xdeadbeef
clock  3  PC=2  in pins, 32     ISR <- 0xdeadbeef
clock  4  PC=3  push block      RX FIFO <- ['0xdeadbeef']
clock  5  PC=0  pull block      OSR <- 0xcafebabe
clock  6  PC=1  out pins, 32    pins <- 0xcafebabe
clock  7  PC=2  in pins, 32     ISR <- 0xcafebabe
clock  8  PC=3  push block      RX FIFO <- ['0xdeadbeef', '0xcafebabe']
clock  9  PC=0  pull block      OSR <- 0x12345678
clock 10  PC=1  out pins, 32    pins <- 0x12345678
clock 11  PC=2  in pins, 32     ISR <- 0x12345678
clock 12  PC=3  push block      RX FIFO <- ['0xdeadbeef', '0xcafebabe', '0x12345678']
clock 13  PC=0  pull block      [stalled - TX FIFO empty]
clock 14  PC=0  pull block      [stalled - TX FIFO empty]

TX FIFO remaining: []
RX FIFO contents:  ['0xdeadbeef', '0xcafebabe', '0x12345678']

Loopback verified: all values passed through correctly!
```
