# pio2fst

Creates a Fast Signal Trace (FST) file by emulating a PIO state machine and
observing changes to its registers and GPIO outputs. The resulting file can
then be visualised/analysed using the freely available [GTKWave](https://gtkwave.sourceforge.net/) tool.

By default, the following values are saved to the file:

* Clock cycle
* Program counter
* Scratch registers - X and Y
* GPIO pin values

## Example Usage
Create a file named `example.fst` by emulating the PIO program `example.pio`:

```shell
poetry run pio2fst --input example.pio --samples 100
gtkwave out.fst
```
