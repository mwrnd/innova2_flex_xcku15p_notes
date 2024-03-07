# Debug Notes



## Delay Motherboard Boot Using RESET Capacitor

Slowing down BIOS boot is a simple trick that solves many PCIe issues. You can do this by pressing the POWER button, then pressing and holding the RESET button for a second before releasing it. Or, connect a capacitor across the reset pins of your motherboard's [Front Panel Header](https://www.intel.com/content/www/us/en/support/articles/000007309/intel-nuc.html). This prevents you from using the RESET button as that would short the capacitor. Try capacitors with values such as 330uF or 680uF. Optimal value depends on required delay and motherboard design.

![Delay Motherboard Boot Using RESET Capacitor](img/Delay_Boot_Using_Capacitor.jpg)

The capacitor across RESET works thanks to an [RC Delay](https://en.wikipedia.org/wiki/RC_time_constant) on the reset signal buffer. The [OpenCompute](https://en.wikipedia.org/wiki/Open_Compute_Project) project has a public schematic and the RESET Button is on Pg#151 in *Project_Olympus_Intel_XSP_Schematics_20171016.pdf* found in [`Project_Olympus_Intel_XSP_Collateral.zip`](http://files.opencompute.org/oc/public.php?service=files&t=e969672c57d6e17647adea54f2c3e5a7&download).

![RESET Button Schematic](img/Server_Motherboard_RESET_Button_Schematic.png)

A standard Schmitt-Trigger inverter such as the [SN74LVC1G14](https://www.ti.com/lit/gpn/SN74LVC1G14) has a positive-going threshold voltage of about 1.5V with a 3.3V supply. I have measured 1k-Ohm between the RESET+ pin and the 3.3V ATX Power supply rail. A 330uF capacitor therefore [delays](http://ladyada.net/library/rccalc.html) boot by about 200ms.

![RC Delay Calculator](img/RC_Delay_Calculator.png)

I found out about this technique [here](https://hackaday.com/2018/02/17/catching-the-pcie-bus/):

![Boot Delay Technique Source](img/Delay_Boot_with_Capacitor_Across_PC_RESET.png)




## Recreating innova2_flex_app Functionality for latest MLNX OFED

[MLNX_OFED](https://network.nvidia.com/products/infiniband-drivers/linux/mlnx_ofed/) versions > 5.2 do not include `mlx5_fpga_tools` which is required by `innova2_flex_app` to program the FPGA, switch the active image, and enable/disable JTAG.

Check if your current kernel supports tracing.
```
cat /boot/config-`uname -r` | grep -e "CONFIG_FUNCTION[[:print:]]*TRACER\|CONFIG_KPROBES"
```

Results should be:
```
CONFIG_FUNCTION_TRACER=y
CONFIG_FUNCTION_GRAPH_TRACER=y
CONFIG_KPROBES=y
CONFIG_KPROBES_ON_FTRACE=y
```

I used [ftrace](https://www.kernel.org/doc/html/latest/trace/ftrace.html) ([Quick Introduction](https://opensource.com/article/21/7/linux-kernel-ftrace)) to figure out the call tree when JTAG is enabled in `innova2_flex_app`.

```
sudo su
cd /sys/kernel/tracing
ps aux | grep innova
echo PID_FROM_ABOVE > set_ftrace_pid
echo function_graph > current_tracer
cat trace > /home/fpga/trace_enablejtag
### run a command in innova2_flex_app now
echo nop > current_tracer
exit
```

![Tracing innova2_flex_app during JTAG Enable](img/tracing_innova2_flex_app_Enable_JTAG.png)

The results show that the `mlx5_core_access_reg` from the `mlx5_core` driver is the function that changes JTAG status.

![Results of tracing innova2_flex_app](img/trace_Enable_JTAG.png)

I then used a [kprobe event tracer](https://www.kernel.org/doc/html/latest/trace/kprobetrace.html) ([Quick Introduction](https://events19.linuxfoundation.org/wp-content/uploads/2017/12/oss-eu-2018-fun-with-dynamic-trace-events_steven-rostedt.pdf)) to figure out the arguments to `mlx5_core_access_reg`.

```
sudo su
cd /sys/kernel/tracing
echo 'p:myprobe mlx5_core_access_reg dev=$arg1:x64 data_in=$arg2:x64 di0=+0($arg2):x32 di1=+4($arg2):x32 di2=+8($arg2):x32 di3=+12($arg2):x32 size_in=$arg3:s32 data_out=$arg4:x64 size_out=$arg5:s32 reg_id=$arg6:x16 arg=$arg7:s32 write=$arg8:s32' > kprobe_events
echo 'r:myretprobe mlx5_core_access_reg ret=$retval'  >> kprobe_events
echo 1 > events/kprobes/myprobe/enable
echo 1 > events/kprobes/myretprobe/enable
echo 1 > tracing_on
## Enable JTAG Access in innova2_flex_app ##
cat trace | grep myprobe
echo 0 > tracing_on
echo 0 > events/kprobes/myprobe/enable
echo 0 > events/kprobes/myretprobe/enable
echo   > kprobe_events  # deletes all probes
exit
```

![Tracing mlx5_core_access_reg](img/tracing_mlx5_core_access_reg_Enable_JTAG.png)

JTAG is enabled by writing `0x900` to register `0x4023`.
```
 innova2_flex_ap-5513    [003] ....  2971.678544: myprobe: (mlx5_core_access_reg+0x0/0x130 [mlx5_core]) dev=0xffff98bed2b40140 data_in=0xffffbc6c03283d08 di0=0x900 di1=0x0 di2=0x0 di3=0x0 size_in=16 data_out=0xffffbc6c03283d18 size_out=16 reg_id=0x4023 arg=0 write=1
```

`mlx5_fpga_ctrl_connect` is in `cmd.c` in the `mlnx-ofed-kernel-5.2` archive.

![mlx5_fpga_ctrl_connect in cmd.c](img/mlx5_fpga_ctrl_connect_in_cmd_c.png)

`mlx5_core_access_reg` is an [EXPORT_SYMBOL](https://lkw.readthedocs.io/en/latest/doc/04_exporting_symbols.html) so it can be called from other kernel modules.

![mlx5_core_access_reg is an EXPORT_SYMBOL](img/mlx5_core_access_reg_is_an_EXPORT_SYMBOL.png)

`MLX5_ST_SZ_DW` sets the value to send.

![MLX5_ST_SZ_DW in driver.h](img/MLX5_ST_SZ_DW_in_driver_h.png)

The values are defined in `mlx_ifc_fpga.h`. The `0x900` is in Little-Endian (`0x00090000` in Big-Endian) so it is written to the `operation[0x8]` bits of the `FPGA_CTRL` register.

![FPGA_CTRL Bit Defines in mlx_ifc_fpga.h](img/mlx_ifc_fpga_h_FPGA_CTRL_Bit_Defines.png)

[`mlxreg`](https://docs.nvidia.com/networking/display/mftv4250/mlxreg+utility) can be used to access registers. By running `innova2_flex_app` in one window and `mlxreg` in another, the `FPGA_CTRL` register can be watched.

```
sudo mst start
sudo mlxreg -d /dev/mst/mt4119_pciconf0 --yes --reg_id 0x4023 --reg_len 0x4 --get
```

![mlxreg after innova2_flex_app Started](img/mlxreg_get_after_innova2_flex_app_Started.png)

After enabling JTAG, the `status[0x8]` bits are `0x3`:

![mlxreg after Enable_JTAG](img/mlxreg_get_after_Enable_JTAG.png)

After enabling the Flex Image, the `flash_select_admin[0x8]` bits are `0x01`:

![mlxreg after Flex Image Active](img/mlxreg_get_after_Flex_Image_Active.png)

Unfortunately, `mlxreg --set` fails with `-E- Failed send access register: ME_ICMD_OPERATIONAL_ERROR` when trying to write the register.
```
sudo mlxreg -d /dev/mst/mt4119_pciconf0 --yes --reg_id 0x4023 --reg_len 0x4 --get
sudo mlxreg -d /dev/mst/mt4119_pciconf0 --yes --reg_id 0x4023 --reg_len 0x4 --set "0x0.16:4=0xA"
sudo mlxreg -d /dev/mst/mt4119_pciconf0 --yes --reg_id 0x4023 --reg_len 0x4 --set "0x0.16:4=0x9"
echo Try to set reserved bits:
sudo mlxreg -d /dev/mst/mt4119_pciconf0 --yes --reg_id 0x4023 --reg_len 0x4 --set "0x0.12:4=0x9"
```

![mlxreg Register Write Fails](img/mlxreg_Register_Write_Fails.png)


### Using mstreg to write FPGA Control Register

`mstreg` from [**mstflint v4.26.0-1**](https://github.com/Mellanox/mstflint/releases/tag/v4.26.0-1) is able to write the FPGA Control registers.

```
wget https://github.com/Mellanox/mstflint/releases/download/v4.26.0-1/mstflint-4.26.0-1.tar.gz
tar -xvf mstflint-4.26.0-1.tar.gz
cd mstflint-4.26.0
./configure --enable-adb-generic-tools --enable-rdmem
make
cd mlxreg/
lspci | grep Mellanox | grep Ethernet
sudo find / * -name register_access_table.adb
```

![mstflint compile and prepare](img/mstreg_compile_and_prepare.png)

Note the Ethernet Controller PCIe address, `04:00.0` above, and the ADB File location, `usr/share/mft/prm_dbs/hca/ext/register_access_table.adb` above.


#### Enable or Disable JTAG Connector

`mstreg` can be used to *DISCONNECT* the FPGA's JTAG from the ConnectX-5 to enable the board's JTAG header to be used.

```
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --get
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --set "0x0.16:4=0x9"
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --get
```

![mstreg DISCONNECT to Enable JTAG](img/mstreg_DISCONNECT_to_Enable_JTAG.png)

Similarly, writing the `4`-bit value `0xA` at the `16`th bit position of register `0x0` connects JTAG signals to the ConnectX-5 and disables the board's JTAG header.
```
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --get
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --set "0x0.16:4=0xA"
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --get
```


#### Set Active FPGA Configuration Bitstream Image

The [FPGA Configuration Memory Layout](https://docs.nvidia.com/networking/display/innova2flex/using+the+mellanox+innova-2+flex+open+bundle#src-11995976_UsingtheMellanoxInnova2FlexOpenBundle-FlashFormat) allows for 3 configuration bitstreams, *Factory*, *User*, and *Flex*.

![FPGA Configuration Memory Layout](../img/FPGA_Configuration_Memory_Layout.png)

When the User Image is scheduled using `innova2_flex_app` under *MLNX_OFED 5.2*, `0x00030000` is written to word `0` of the control register `0x4023`.

![kprobe of Set User Image Active](img/kprobe_Set_User_Image_Active.png)

When the Flex Image is scheduled using `innova2_flex_app` under *MLNX_OFED 5.2*, `0x00030001` is written to word `0` of the control register `0x4023`.

![kprobe of Set Flex Image Active](img/kprobe_Set_Flex_Image_Active.png)

The User Image can be activated using `mstreg`:

```
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --get
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --set "0x0.16:4=0x3,0x4.16:4=0x1"
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --get
```

![mstreg Set User Image Active](img/mstreg_Set_User_Image_Active.png)

The Flex Image can be activated using `mstreg`:

```
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --get
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --set "0x0.16:4=0x3,0x4.16:4=0x0"
sudo ./mstreg --yes --device 04:00.0 --adb_file /usr/share/mft/prm_dbs/hca/ext/register_access_table.adb --reg_id 0x4023 --reg_len 0x8 --get
```

![mstreg Set Flex Image Active](img/mstreg_Set_Flex_Image_Active.png)




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


### Waveshare Platform Cable USB Clone

The [Waveshare Platform USB Cable clone](https://www.waveshare.com/platform-cable-usb.htm) is also based on an [FX2 USB MCU](https://www.infineon.com/cms/en/product/universal-serial-bus/usb-2.0-peripheral-controllers/ez-usb-fx2lp-fx2g2-usb-2.0-peripheral-controller/) but instead uses a [Lattice MachXO2 CPLD](https://www.latticesemi.com/Products/FPGAandCPLD/MachXO2).

![Waveshare Platform USB Cable](img/Waveshare_Platform_USB_Cable_PCB_Top.jpg)




