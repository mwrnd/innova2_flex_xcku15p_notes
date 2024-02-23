# Innova2 Hardware Notes




## Innova2 4GB MNV303212A-ADIT Hardware Notes


### Testing MNV303212A-ADIT OpenCAPI Connections

A [`v0.1-alpha` **OpenCAPI_Breakout**](https://github.com/mwrnd/OpenCAPI_Breakout/releases/tag/v0.1-alpha) board and the [IBERT for GTY](https://docs.xilinx.com/v/u/en-US/pg196-ibert-ultrascale-gty) can be used to test OpenCAPI port connections. Testing works well using a [3M 8ES8-1DF21 Cable](https://www.trustedparts.com/en/search/8ES8-1DF21)([Datasheet](https://multimedia.3m.com/mws/media/1398233O/3m-slimline-twin-ax-assembly-sff-8654-x8-30awg-78-5100-2665-8.pdf)).

![Testing Innova2 OpenCAPI GTY Connections](img/Innova2_4GB_MNV303212A-ADIT_Testing_OpenCAPI_GTY.jpg)

A [PCIe_x8_Breakout](https://github.com/mwrnd/PCIe_x8_Breakout) in a PCIe socket was used as the source of the OpenCAPI 100MHz `GTREFCLK` clock.

![PCIe Socket Used as Clock Source](img/Innova2_4GB_ADIT_Testing_OpenCAPI_GTY-PCIe_as_Clock_Source.jpg)

I manually searched for working connections.

![U.FL Cable connecting two Channels](img/Innova2_4GB_ADIT_Testing_OpenCAPI_GTY-Connections.jpg)

After finding working connections I connected both N and P signals.

![Connect both N and P Signals](img/Innova2_4GB_ADIT_Testing_OpenCAPI_RX1p-TX3p_RX1n-TX3n.jpg)

I discovered that the Innova2 4GB MNV303212A-AD**I**T has a significantly different OpenCAPI pinout than the Innova2 8GB MNV303212A-AD**L**T.
```
X0Y16: RX3p-TX0n, RX3n-TX0p
X0Y17: RX0p-TX1n, RX0n-TX1p
X0Y18: RX2p-TX2p, RX2n-TX2n
X0Y20: RX4p-TX4n, RX4n-TX4p
X0Y21: RX5p-TX5p, RX5n-TX5n
X0Y22: RX6p-TX6p, RX6n-TX6n
X0Y23: RX7p-TX7p, RX7n-TX7n
```

The following are Eye Diagram Scans for all the OpenCAPI GTY Channels:

`X0Y16 RX3n-TX0p`-only:

![IBERT Results for X0Y16 RX3n-TX0p](img/ADIT_OpenCAPI_X0Y16_RX3n-TX0p.png)

`X0Y16 RX3p-TX0n RX3n-TX0p`:

![IBERT Results for X0Y16 RX3p-TX0n RX3n-TX0p](img/ADIT_OpenCAPI_X0Y16_RX3p-TX0n_RX3n-TX0p.png)

`X0Y17 RX0p-TX1n RX0n-TX1p`:

![IBERT Results for X0Y17 RX0p-TX1n RX0n-TX1p](img/ADIT_OpenCAPI_X0Y17_RX0p-TX1n_RX0n-TX1p.png)

`X0Y18 RX2p-TX2p RX2n-TX2n`:

![IBERT Results for X0Y18 RX2p-TX2p RX2n-TX2n](img/ADIT_OpenCAPI_X0Y18_RX2p-TX2p_RX2n-TX2n.png)

`X0Y19 RX1p-TX3p RX1n-TX3n`:

![IBERT Results for X0Y19 RX1p-TX3p RX1n-TX3n](img/ADIT_OpenCAPI_X0Y19_RX1p-TX3p_RX1n-TX3n.png)

`X0Y20 RX4p-TX4n RX4n-TX4p`:

![IBERT Results for X0Y20 RX4p-TX4n RX4n-TX4p](img/ADIT_OpenCAPI_X0Y20_RX4p-TX4n_RX4n-TX4p.png)

`X0Y21 RX5p-TX5p RX5n-TX5n`:

![IBERT Results for X0Y21 RX5p-TX5p RX5n-TX5n](img/ADIT_OpenCAPI_X0Y21_RX5p-TX5p_RX5n-TX5n.png)

`X0Y22 RX6p-TX6p RX6n-TX6n`:

![IBERT Results for X0Y22 RX6p-TX6p RX6n-TX6n](img/ADIT_OpenCAPI_X0Y22_RX6p-TX6p_RX6n-TX6n.png)

`X0Y23 RX7p-TX7p RX7n-TX7n`:

![IBERT Results for X0Y23 RX7p-TX7p RX7n-TX7n](img/ADIT_OpenCAPI_X0Y23_RX7p-TX7p_RX7n-TX7n.png)






## Innova2 8GB MNV303212A-ADLT Hardware Notes


### Testing MNV303212A-ADLT OpenCAPI Connections

A [`v0.1-alpha` **OpenCAPI_Breakout**](https://github.com/mwrnd/OpenCAPI_Breakout) board and the [IBERT for GTY project](LINKMISSING) can be used to confirm OpenCAPI port pinout and connections. Testing works well using a [3M Cable](LINKMISSING).

![Testing Innova2 OpenCAPI GTY Connections](img/Innova2_4GB_MNV303212A-ADIT_Testing_OpenCAPI_GTY.jpg)

A [PCIe_x8_Breakout](https://github.com/mwrnd/PCIe_x8_Breakout) in a PCIe socket was used as the source of the OpenCAPI 100MHz `GTREFCLK` clock.

![PCIe Socket Used as Clock Source](img/Innova2_4GB_ADIT_Testing_OpenCAPI_GTY-PCIe_as_Clock_Source.jpg)

I manually searched for working connections.

![U.FL Cable connecting two Channels](img/Innova2_4GB_ADIT_Testing_OpenCAPI_GTY-Connections.jpg)

After finding working connections I connected both N and P signals.

![Connect both N and P Signals](img/Innova2_4GB_ADIT_Testing_OpenCAPI_RX1p-TX3p_RX1n-TX3n.jpg)

I discovered channels 0, 3, and 4 have swapped transceiver differential pairs (N,P):
```
RX0p-TX0n, RX0n-TX0p
RX1p-TX1p, RX1n-TX1n
RX2p-TX2p, RX2n-TX2n
RX3p-TX3n, RX3n-TX3p
RX4p-TX4n, RX4n-TX4p
RX5p-TX5p, RX5n-TX5n
RX6p-TX6p, RX6n-TX6n
RX7p-TX7p, RX7n-TX7n
```

The following are Eye Diagram Scans for all the OpenCAPI GTY Channels:

`X0Y16 RX0p-TX0n RX0n-TX0p`:

![IBERT Results for X0Y16 RX0p-TX0n RX0n-TX0p](img/ADLT_OpenCAPI_X0Y16_RX0p-TX0n_RX0n-TX0p.png)

`X0Y17 RX1p-TX1p RX1n-TX1n`:

![IBERT Results for X0Y17 RX1p-TX1p RX1n-TX1n](img/ADLT_OpenCAPI_X0Y17_RX1p-TX1p_RX1n-TX1n.png)

`X0Y18 RX2p-TX2p RX2n-TX2n`:

![IBERT Results for X0Y18 RX2p-TX2p RX2n-TX2n](img/ADLT_OpenCAPI_X0Y18_RX2p-TX2p_RX2n-TX2n.png)

`X0Y19 RX3p-TX3n RX3n-TX3p`:

![IBERT Results for X0Y19 RX3p-TX3n RX3n-TX3p](img/ADLT_OpenCAPI_X0Y19_RX3p-TX3n_RX3n-TX3p.png)

`X0Y20 RX4p-TX4n RX4n-TX4p`:

![IBERT Results for X0Y20 RX4p-TX4n RX4n-TX4p](img/ADLT_OpenCAPI_X0Y20_RX4p-TX4n_RX4n-TX4p.png)

`X0Y21 RX5p-TX5p RX5n-TX5n`:

![IBERT Results for X0Y21 RX5p-TX5p RX5n-TX5n](img/ADLT_OpenCAPI_X0Y21_RX5p-TX5p_RX5n-TX5n.png)

`X0Y22 RX6p-TX6p RX6n-TX6n`:

![IBERT Results for X0Y22 RX6p-TX6p RX6n-TX6n](img/ADLT_OpenCAPI_X0Y22_RX6p-TX6p_RX6n-TX6n.png)

`X0Y23 RX7p-TX7p RX7n-TX7n`:

![IBERT Results for X0Y23 RX7p-TX7p RX7n-TX7n](img/ADLT_OpenCAPI_X0Y23_RX7p-TX7p_RX7n-TX7n.png)

After about 15 minutes Channel X0Y19 began failing:

![X0Y19 begins failing after 15min](img/ADLT_OpenCAPI_X0Y19_RX3_TX3_after_15min.png)

Results are much worse for each channel when using an SFPCables SlimSAS cable:

![IBERT Results for X0Y19 Using SFPCables Cable](img/ADLT_OpenCAPI_X0Y19_Using_SFPCables_Cable.png)

The PLL loses lock.

![PLL Lock Lost Using SFPCables Cable](img/ADLT_OpenCAPI_X0Y16_Using_SFPCables_Cable_PLL_Lock_Lost.png)




