from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform, VivadoProgrammer

_io = [
    #("cpu_reset", 0, Pins("A10"), IOStandard("LVCMOS33"), Misc("PULLDOWN true")),

    # SYS clock 100 MHz (input) signal. The sys_clk_p and sys_clk_n
    # signals are the PCI Express reference clock.
    #("clk100", 0,
    #    Subsignal("p", Pins("B6")),
    #    Subsignal("n", Pins("B5"))
    #),
    ("clk100", 0,
        Subsignal("p", Pins("B6")),
        Subsignal("n", Pins("B5"))
    ),
    ("user_led", 0, Pins("V12"), IOStandard("LVCMOS33"), Drive(8), Misc("PULLUP true")),
    ("user_led", 1, Pins("V11"), IOStandard("LVCMOS33"), Drive(8), Misc("PULLUP true")),
    ("user_led", 2, Pins("V13"), IOStandard("LVCMOS33"), Drive(8), Misc("PULLUP true")),
    ("user_led", 3, Pins("V14"), IOStandard("LVCMOS33"), Drive(8), Misc("PULLUP true")),

    ("led2", 0, Pins("V3"), IOStandard("LVCMOS33"), Drive(8), Misc("PULLUP true")),

    ("serial", 0,
        Subsignal("tx", Pins("K1")),
        Subsignal("rx", Pins("K2")),
        IOStandard("LVCMOS33")
    ),
    ("pcie_x1", 0,
        Subsignal("rst_n", Pins("A10"), IOStandard("LVCMOS33"), Misc("PULLDOWN true")),
        Subsignal("clk_p", Pins("D6")),
        Subsignal("clk_n", Pins("D5")),
        Subsignal("rx_p", Pins("G4")),
        Subsignal("rx_n", Pins("G3")),
        Subsignal("tx_p", Pins("B2")),
        Subsignal("tx_n", Pins("B1")),
        Subsignal("clk_req_n", Pins("A9"), IOStandard("LVCMOS33"), Misc("PULLDOWN true"))
    ),
    ## SYS reset (input) signal.  The sys_reset_n signal is generated
    ## by the PCI Express interface (PERST#).
    #set_property PACKAGE_PIN A10 [get_ports sys_rst_n]
    #set_property IOSTANDARD LVCMOS33 [get_ports sys_rst_n]
    #set_property PULLDOWN true [get_ports sys_rst_n]
]

_connectors = []

class Platform(XilinxPlatform):
    name = "picoevb"
    default_clk_name = "clk100"
    default_clk_period = 1e9/100e6

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7a50t-csg325-2", _io, _connectors, toolchain="vivado")
        self.add_platform_command("set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets pcie_x1_rst_n_IBUF]")
        self.toolchain.bitstream_commands = [
            "set_property BITSTREAM.CONFIG.OVERTEMPPOWERDOWN ENABLE [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGRATE 66 [current_design]",
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "set_property BITSTREAM.CONFIG.SPI_FALL_EDGE YES [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]",
            "set_property CONFIG_VOLTAGE 3.3 [current_design]",
            "set_property CFGBVS VCCO [current_design]"
        ]
        self.toolchain.additional_commands = \
            ["write_cfgmem -force -format bin -interface spix4 -size 16 "
             "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.bin"]

    def create_programmer(self):
        return VivadoProgrammer(flash_part="s25fl132k-spi-x1_x2_x4")

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)