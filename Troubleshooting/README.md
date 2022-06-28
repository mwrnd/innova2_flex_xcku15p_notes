# Troubleshooting Innova-2 Flex XCKU15P FPGA Designs

## Troubleshooting DDR4

### DDR4 Communication Error

If you attempt to send data to the DDR4 address but get `write file: Unknown error 512` it likely means DDR4 did not initialize properly. Start by performing a cold reboot and checking communication again. If [BRAM and GPIO communication](https://github.com/mwrnd/innova2_xcku15p_ddr4_bram_gpio#axi-bram-communication) succeed but DDR4 fails then the issue is with DDR4.
```Shell
cd ~/dma_ip_drivers/XDMA/linux-kernel/tools/
dd if=/dev/urandom bs=1 count=8192 of=TEST
sudo ./dma_to_device   --verbose --device /dev/xdma0_h2c_0 --address 0x0 --size 8192  -f    TEST
```

![Error 512](img/XDMA_DDR4_Communication_Failure_Error_512.png)

#### Connect JTAG

Connect JTAG to view calibration status.

![DDR4 JTAG CAL FAIL](img/DDR4_CAL_Fail_Write_Leveling.png)

#### CAL FAIL Write Leveling

A *Write Leveling* failure is unfortunately a hardware issue. Refer to [Xilinx's PG150 Memory IP Guide](https://www.xilinx.com/support/documentation/ip_documentation/ultrascale_memory_ip/v1_4/pg150-ultrascale-memory-ip.pdf).

![CAL FAIL Write Leveling](img/DDR4_PG150_DDR_CAL_ERROR_1.png)

#### Recreating ddr4_0_ex Example Design

The included `ddr4_0_ex_example_design.xdc` constraints file has the correct pin mappings when creating the DDR4 Example Design using **Vivado 2021.2**.

Begin by `source`ing the [innova2_xcku15p_ddr4_bram_gpio](https://github.com/mwrnd/innova2_xcku15p_ddr4_bram_gpio#recreating-the-design-in-vivado) project and editing the DDR4 options to slower memory speeds (**1250ps**) and the built-in IC configuration (**MT40A1G16WBU-083E**).

![DDR4 Basic Options](img/DDR4_Troubleshooting_Options_Setup.png)

Right-click on the DDR4 Block and choose *Generate Example Design*. After Vivado generates the Example Design, update the Constraints File *example_design.xdc* with the contents of the included `ddr4_0_ex_example_design.xdc` file. Also, the `sys_rst` signal must be inverted in *example_top.sv*.

![Invert sys_rst](img/ddr4_0_ex_Inverted_PCIe_Reset_for_sys_rst.png)


#### JTAG Communication with ddr4_0_ex Example Design

Xilinx's *ddr4_0_ex* Example Design includes additional testing infrastructure.

![JTAG ddr4_0_ex Example Design](img/DDR4_CAL_Fail_Hardware_Manager_ddr4_0_ex.png)

