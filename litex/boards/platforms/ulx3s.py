# This file is Copyright (c) 2018 Florent Kermarrec <florent@enjoy-digital.fr>
# License: BSD

from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform


_io = [
    ("clk25", 0, Pins("G2"), IOStandard("LVCMOS33")),
    ("rst", 0, Pins("R1"), IOStandard("LVCMOS33")),

    ("user_led", 0, Pins("B2"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("C2"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("C1"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("D2"), IOStandard("LVCMOS33")),
    ("user_led", 0, Pins("D1"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("E2"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("E1"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("H3"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("L4"), IOStandard("LVCMOS33")),
        Subsignal("rx", Pins("M1"), IOStandard("LVCMOS33"))
    ),

    ("sdram_clock", 0, Pins("F19"), IOStandard("LVCMOS33")),
    ("sdram", 0,
        Subsignal("a", Pins("M20 M19 L20 L19 K20 K19 K18 J20 J19 H20 N19 G20 G19")),
        Subsignal("dq", Pins("J16 L18 M18 N18 P18 T18 T17 U20 E19 D20 D19 C20 E18 F18 J18 J17")),
        Subsignal("we_n", Pins("T20")),
        Subsignal("ras_n", Pins("R20")),
        Subsignal("cas_n", Pins("T19")),
        Subsignal("cs_n", Pins("P20")),
        Subsignal("cke", Pins("F20")),
        Subsignal("ba", Pins("P19 N20")),
        Subsignal("dm", Pins("U19 E20")),
        IOStandard("LVCMOS33")
    ),

    ("wifi_gpio0", 0, Pins("L2"), IOStandard("LVCMOS33")),
]


class Platform(LatticePlatform):
    default_clk_name = "clk100"
    default_clk_period = 10

    def __init__(self, **kwargs):
        LatticePlatform.__init__(self, "LFE5U-45F-6BG381C", _io, **kwargs)
