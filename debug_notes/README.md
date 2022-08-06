# Debug Notes

## Debugging Vivado xsdb xsct JTAG Errors

If commands in `xsdb` lead to a Memory Write Errors or Debug Transport Module errors:
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

