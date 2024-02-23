# Debug Notes

## Delay Motherboard Boot Using RESET Capacitor

Slowing down BIOS boot is a simple trick that solves many PCIe issues. You can do this by pressing the POWER button, then pressing and holding the RESET button for a second before releasing it. Or, connect a capacitor across the reset pins of your motherboard's [Front Panel Header](https://www.intel.com/content/www/us/en/support/articles/000007309/intel-nuc.html). This prevents you from using the RESET button as that would short the capacitor. Try values between 100uF and 1000uF. Optimal value depends on required delay and motherboard design.

![Delay Motherboard Boot Using RESET Capacitor](img/Delay_Boot_Using_Capacitor.jpg)

The capacitor across RESET works thanks to an [RC Delay](https://en.wikipedia.org/wiki/RC_time_constant) on the reset signal buffer. The [OpenCompute](https://en.wikipedia.org/wiki/Open_Compute_Project) project has a public schematic and the RESET Button is on Pg#151 in *Project_Olympus_Intel_XSP_Schematics_20171016.pdf* found in [`Project_Olympus_Intel_XSP_Collateral.zip`](http://files.opencompute.org/oc/public.php?service=files&t=e969672c57d6e17647adea54f2c3e5a7&download).

![RESET Button Schematic](img/Server_Motherboard_RESET_Button_Schematic.png)

A standard Schmitt-Trigger inverter such as the [SN74LVC1G14](https://www.ti.com/lit/gpn/SN74LVC1G14) has a positive-going threshold voltage of about 1.5V with a 3.3V supply. I have measured 1k-Ohm between the RESET+ pin and the 3.3V ATX Power supply rail. A 330uF capacitor [delays](http://ladyada.net/library/rccalc.html) boot by about 200ms.

![RC Delay Calculator](img/RC_Delay_Calculator.png)

I found out about this technique [here](https://hackaday.com/2018/02/17/catching-the-pcie-bus/):

![Boot Delay Technique Source](img/Delay_Boot_with_Capacitor_Across_PC_RESET.png)




## Discerning ADLT vs ADAT and ADIT Variants

[Innova2 8GB MNV303212A-ADLT](https://www.mellanox.com/files/doc-2020/pb-innova-2-flex.pdf) boards have [`MT40A1G16KNR-075`](https://media-www.micron.com/-/media/client/global/documents/products/data-sheet/dram/ddr4/ddr4_16gb_x16_1cs_twindie.pdf) DDR4 ICs with [**D9WFR** FBGA Code](https://www.micron.com/support/tools-and-utilities/fbga?fbga=D9WFR#pnlFBGA). [Innova2 4GB MNV303212A-ADAT/MNV303212A-ADIT](https://network.nvidia.com/pdf/eol/LCR-000437.pdf) boards have [`MT40A512M16JY-083E`](https://media-www.micron.com/-/media/client/global/documents/products/data-sheet/dram/ddr4/8gb_ddr4_sdram.pdf) DDR4 ICs with [**D9TBK** FBGA Code](https://www.micron.com/support/tools-and-utilities/fbga?fbga=D9TBK#pnlFBGA).

![DDR4 IC Comparison](img/Innova2_Variant_DDR4_Comparison.jpg)




## Tracing OpenCAPI Connector Signals

![Partial Tracing of OpenCAPI Signals](img/Innova2_ADLT_OpenCAPI_Partial_Pinout.jpg)

![Back of Board](img/Innova2_ADLT_OpenCAPI_Back_of_Board.jpg)




## Debugging Vivado xsdb xsct JTAG Errors

If commands in `xsdb` lead to Memory Write Errors or Debug Transport Module errors:
```Shell
Failed to download /home/user/boot.elf
Memory write error at 0x8022D500. FPGA reprogrammed, wait for debugger resync
xsdb% Info: Hart #0 (target 3) Stopped at 0x10dd4 (Suspended)
...
Failed to download vivado-risc-v/workspace/boot.elf
Memory write error at 0x80000100. Debug Transport Module timeout
xsdb% Info: Hart #0 (target 3) Running (Debug Transport Module: data corruption (ID))
```

Edit the `xsdb.tcl` script to add debug logging to the call to `exec $server ...` which is on line 2986 in Vivado 2021.2's `xsdb`:
```Shell
sudo gedit /tools/Xilinx/Vivado/2021.2/scripts/xsdb/xsdb/xsdb.tcl
```

The core JTAG-related logging options are:
```Tcl
-l protocol,context,jtag,jtag2 -L hw_server_log_xsdb
```

Logging *everything* is also an option but the log file generates about 5MB/sec:
```
-l alloc,eventcore,waitpid,events,protocol,context,children,discovery,asyncreq,proxy,tcflog,elf,stack,plugin,shutdown,disasm,jtag,jtag2,slave,dpc -L hw_server_log_xsdb
```

![Edit xsdb.tcl to enable JTAG Debug](img/Edit_xsdb_tcl_to_enable_JTAG_Debug.png)

To interleave JTAG log data with `xsdb`, its `stdout` and `stderr` can be append-redirected to the log file `>>`.
```Shell
source /tools/Xilinx/Vivado/2021.2/settings64.sh
/tools/Xilinx/Vitis/2021.2/bin/unwrapped/lnx64.o/rlwrap -rc -f /tools/Xilinx/Vitis/2021.2/scripts/xsdb/xsdb/cmdlist /tools/Xilinx/Vitis/2021.2/bin/loader -exec rdi_xsdb  >>hw_server_log_xsdb  2>>hw_server_log_xsdb
```

However, this means commands must be sent blindly to `xsdb`. Try running a regular interactive `xsdb` session prior to a logging session to get a sense of the delay required between commands.
```
connect
targets 3
dow boot.elf
exit
```

![xsdb with logging](img/xsdb_into_hw_server_log_xsdb.png)

It is possible to redirect `xsdb` output to both the screen and the log file but usage is messy. Lines are repeated or disappear.
```Shell
(/tools/Xilinx/Vitis/2021.2/bin/unwrapped/lnx64.o/rlwrap -rc -f /tools/Xilinx/Vitis/2021.2/scripts/xsdb/xsdb/cmdlist /tools/Xilinx/Vitis/2021.2/bin/loader -exec rdi_xsdb 2>  >(tee -a /dev/stderr)) | tee -a hw_server_log_xsdb
```

![xsdb interactive with logging](img/xsdb_into_hw_server_log_xsdb_interactive.png)

Edit `hw_server_log_xsdb` and look for the `Memory write` error:

![Edit hw_server_log_xsdb](img/vi_hw_server_log_xsdb.png)

The above notes are a result of working on [`eugene-tarassov/vivado-risc-v` Issue 97](https://github.com/eugene-tarassov/vivado-risc-v/issues/97).




## Debugging PCIe Using Xilinx IBERT

**Work-In-Progress**

![SlimSAS to PCIe Testing](img/SlimSAS_to_PCIe_Testing.jpg)

Create an `xdma_0_ex` example design with all debugging options enabled. Connect a JTAG debugger to the board and run `source test_rd.tcl` in the [**Tcl Console**](https://docs.xilinx.com/r/2021.1-English/ug893-vivado-ide/Using-the-Tcl-Console). It will be in the `xdma_0_ex/xdma_0_ex.gen/sources_1/ip/xdma_0/ip_0/xdma_0_pcie4_ip/pcie_debugger` directory. Refer to the [IBERT Product Guide](https://docs.xilinx.com/v/u/en-US/pg246-in-system-ibert).

![source test_rd.tcl](img/Innova2_PCIe_xdma_0_ex_source_test_rd_tcl.png)

In your OS's terminal, `cd` into the `xdma_0_ex/xdma_0_ex.gen/sources_1/ip/xdma_0/ip_0/xdma_0_pcie4_ip/pcie_debugger` directory and run the various state diagrams.
```
tclsh draw_ltssm.tcl
tclsh draw_reset.tcl
```

![Draw LTSSM](img/Innova2_PCIe_xdma_0_ex_tclsh_draw_ltssm.jpg)

![Draw Reset](img/Innova2_PCIe_xdma_0_ex_tclsh_draw_reset.png)

Run a Sweep in Vivado to see an [Eye Diagram](https://en.wikipedia.org/wiki/Eye_pattern).

![Run a Sweep to see an Eye Diagram](img/Innova2_PCIe_SlimSAS_Eye_Diagram.png)




## Useful Hardware for Debug

A PCIe x16-to-x1 Adapter forces x1 lane width.

![PCIe x16 to x1 Adapter](img/PCIe_x16-to-x1_Adapter.jpg)

A PCIe Extender can be used to solder directly to individual lanes.

![PCIe x1 Extender for Direct Lane Soldering](img/PCIe_x1_Extender_Solder_Direct_to_Specific_Lane.jpg)




## Platform Cable for JTAG

### Xilinx DLC10 Platform Cable USB II

The [Xilinx Platform Cable USB II](https://docs.xilinx.com/v/u/en-US/ds593) is based on an [FX2 USB MCU](https://www.infineon.com/cms/en/product/universal-serial-bus/usb-2.0-peripheral-controllers/ez-usb-fx2lp-fx2g2-usb-2.0-peripheral-controller/) and [Spartan-3 FPGA](https://www.xilinx.com/products/silicon-devices/fpga/spartan-3.html).

![Xilinx DLC10 Platform Cable USB II PCB Top](img/Xilinx_DLC10_Platform_Cable_USB_II_PCB.jpg)


### Xilinx DLC10 Platform Cable USB II

The [Waveshare Platform USB Cable clone](https://www.waveshare.com/platform-cable-usb.htm) is also based on an [FX2 USB MCU](https://www.infineon.com/cms/en/product/universal-serial-bus/usb-2.0-peripheral-controllers/ez-usb-fx2lp-fx2g2-usb-2.0-peripheral-controller/) but instead uses a [Lattice MachXO2 CPLD](https://www.latticesemi.com/Products/FPGAandCPLD/MachXO2).

![Waveshare Platform USB Cable](img/Waveshare_Platform_USB_Cable_PCB_Top.jpg)




