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


