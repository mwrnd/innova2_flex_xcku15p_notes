# Under Linux, run   sudo rmmod hid_mcp2221   to remove MCP2221 HID driver
# Using Raspberry Pi Pico running pico_i2c_sniffer to capture I2C Bus

import EasyMCP2221

# Connect to MCP2221
mcp = EasyMCP2221.Device()
mcp.I2C_speed(400000)

# Optionally configure GP3 to show I2C bus activity.
mcp.set_pin_function(gp3 = "LED_I2C")

# 0x40 << 1 == 0x80
addr=0x40

"""
I2C Bus Capture during Boot when running Flex Image:

s80a00a00a00a00a00a90a00a0Cas81a00a00a00a04np
s80a00a00a00a00a00a90a00a10as81a00a00a00a0Anp
s80a00a00a00a00a00a90a00a00as81a00a00a00aC1np
s80a00a00a00a00a00a90a00a04as81a27a11a20a18np
s80a00a00a00a00a00a90a00a08as81a00a11a56a32np
s80a00a00a00a00a00a90a00a14as81a8BaADaF0a0Dnp
s80a00a00a00a00a00a90a00a1Cas81a8BaADaF0a0Dnp
s80a00a00a00a00a00a90a00a18as81a8BaADaF0a0Dnp
s80a8BaADaF0a0Da8BaADaF0a0Das81a00a00a00a00np
s80a00a00a00a00a00a90a00a1Cas81a8BaADaF0a0Dnp
s80a00a00a00a00a00a90a00a18as81a8BaADaF0a0Dnp
s80a8BaADaF0a0Da8BaADaF0a11as81a00a00a00a00np
s80a00a00a00a00a00a90a00a1Cas81a8BaADaF0a0Dnp
s80a00a00a00a00a00a90a00a18as81a8BaADaF0a0Dnp
s80a8BaADaF0a0Da8BaADaF0a15as81a00a00a00a00np
s80a00a00a00a00a00a90a00a20as81a8BaADaF0a0Dnp
s80a00a00a00a00a00a90a00a24as81a8BaADaF0a0Dnp
s80a00a00a00a00a00a90a00a28as81a8BaADaF0a0Dnp
s80a00a00a00a00a00a90a00a2Cas81a8BaADaF0a0Dnp
s80a00a00a00a00a00a90a00a30as81a8BaADaF0a0Dnp
s80a00a00a00a00a00a90a00a34as81a8BaADaF0a0Dnp
"""

# Recreate ConnectX5-FPGA I2C Bus Communication at Boot

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x0C], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x10], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x00], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x04], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x08], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x14], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x1C], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x18], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x8B, 0xAD, 0xF0, 0x0D, 0x8B, 0xAD, 0xF0, 0x0D], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x1C], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x18], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x8B, 0xAD, 0xF0, 0x0D, 0x8B, 0xAD, 0xF0, 0x11], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x1C], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x18], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x8B, 0xAD, 0xF0, 0x0D, 0x8B, 0xAD, 0xF0, 0x15], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x20], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x24], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x28], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x2C], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x30], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x34], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)




"""
I2C Bus Capture when innova2_flex_app Disables JTAG or Sets User Image Active:

s80a00a00a00a00a00a90a00a6Cas81a00a00a00a02np

"""
r = mcp.I2C_read(addr, size = 1, kind = "regular") # seperator

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, 0x6C], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)



"""
I2C Bus Capture when innova2_flex_app Changes Power Consumption:

s80a00a00a00a00a00a00a00a24as81a00a00a00a00np

"""
r = mcp.I2C_read(addr, size = 1, kind = "regular") # seperator

r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x24], kind = "nonstop", timeout_ms = 20)
r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
print(r)


# Most Flex Image I2C registers seem to be at address 0x00000000009000xx but nothing new shows up
r = mcp.I2C_read(addr, size = 1, kind = "regular") # seperator

for reg in range(0, 0xFF, 4):
    r = mcp.I2C_write(addr, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x00, reg], kind = "nonstop", timeout_ms = 20)
    r = mcp.I2C_read(addr, size = 4, kind = "restart", timeout_ms = 20)
    print('0x%(regnum)02X' % {'regnum': reg}, ": ", r)


