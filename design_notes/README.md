# Design Notes

## UltraRAM

The [Ultrascale+ FPGA Product Selection Guide](https://docs.xilinx.com/v/u/en-US/ultrascale-plus-fpga-product-selection-guide) lists the XCKU15P as having 36Mbit of UltraRAM:

![UltraScale+ Product Selection Guide KU15P](img/KU15P_Product_Selection_Info.png)

All the UltraRAM is in a single column which can be seen when an Implemented design is opened in Vivado:

![XCKU15P Implemented Design View of URAM Blocks](img/XCKU15P_Implemented_Design_View_URAM_Blocks.png)

UltraRAM can be [cascaded (ug573)](https://docs.xilinx.com/v/u/en-US/ug573-ultrascale-memory-resources) and `(36000000/8/1024/1024)~=4.29` so 4MByte of range should be possible when using UltraRAM but some versions of Vivado fail implementation.

![UltraScale UltraRAM Blocks can be Cascaded](img/UltraScale_UltraRAM_Blocks.png)

2MB of URAM running at about 220MHz is the maximal usable single URAM BRAM Block that will consistently pass implementation.

![UltraRAM Range is 2M](img/BRAM_Controller_UltraRAM_Range_is_2M_for_2MB.png)


## PCIe

The PCIe Reset Pin should be in Bank65 but the Innova-2 has it in Bank90.

![PCIe Reset Pin Should be in Bank65](img/PCIe_RESET_Pin_Should_be_in_Bank65.png)

The PCIe-to-AXI-Lite interface has a Translation value which allows you to offset the address of connected AXI devices. For example, if your are using an MCU and its peripherals are above `0x70000000`, you can use that as the offset to allow the BAR Size (1 Megabyte below) to cover all peripheral addresses.

![XDMA AXI-Lite PCIe to AXI Translation](img/XDMA_PCIe_to_AXI-Lite.png)

When you define the number of channels:

![XDMA Number of Channels](img/XDMA_Number_of_Channels.png)

Each channel will have its own set of `h2c` and `c2h` files.

![XDMA Driver dev Files](../img/XDMA_Driver_dev_Files.png)




## Processor System Reset Block

A [Processor System Reset](https://www.xilinx.com/products/intellectual-property/proc_sys_reset.html) IP Block ([pg164](https://docs.xilinx.com/v/u/en-US/pg164-proc-sys-reset)) includes reset sequencing:

![Processor System Reset Module Sequences Resets](img/Processor_System_Reset_Module_Sequences_Resets.png)




## Alternate Bitstream Programming Methods

Refer to [Post-Configuration Access of SPI Flash Memory (XAPP1280)](https://docs.xilinx.com/r/en-US/xapp1280-us-post-cnfg-flash-startupe3).

![XAPP1280 Bitstream Programming Over UART](img/XAPP1280_Programming_Bitstream_Over_UART.png)




