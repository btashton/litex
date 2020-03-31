#!/usr/bin/env python3

# This file is Copyright (c) 2015-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# License: BSD

import argparse

from migen import *
from migen.genlib.io import CRG, DifferentialInput

from litex.boards.platforms import picoevb

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.uart import UARTWishboneBridge

# CRG ----------------------------------------------------------------------------------------------

class _CRG(Module):
    def __init__(self, platform, sys_clk_freq, clk100, rst, serial):
        self.clock_domains.cd_sys    = ClockDomain()
        #self.clock_domains.cd_sys4x  = ClockDomain(reset_less=True)
        #self.clock_domains.cd_clk200 = ClockDomain()
        #self.clock_domains.cd_clk1 = ClockDomain()

        # # #

        self.submodules.pll = pll = S7MMCM(speedgrade=-2)
        self.comb += pll.reset.eq(rst)
        pll.register_clkin(clk100, 100e6)
        pll.create_clkout(self.cd_sys,    sys_clk_freq)
        #pll.create_clkout(self.cd_sys4x,  4*sys_clk_freq)
        #pll.create_clkout(self.cd_clk200, 200e6)
        #pll.create_clkout(self.cd_clk1, 5e6)

        self.comb += platform.request("user_led", 0).eq(~pll.locked)

        #self.submodules.idelayctrl = S7IDELAYCTRL(self.cd_clk200)

# BaseSoC ------------------------------------------------------------------------------------------

class BaseSoC(SoCCore):

    def __init__(self, sys_clk_freq=int(100e6), with_ethernet=False, **kwargs):
        platform = picoevb.Platform()

        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform,
            clk_freq                 = sys_clk_freq,
            uart_name                = "crossover",
            #uart_name                = "jtag_uart",
            cpu_variant              = "debug",
            integrated_rom_size      = 0x8000,
            integrated_main_ram_size = 0x8000,
            **kwargs)

        # CRG --------------------------------------------------------------------------------------

        clk100_pads = platform.request("clk100")
        #uart = platform.request("serial")
        clk100_sig = Signal()
        clk100_buf = Signal()
        self.specials += [
            Instance("IBUFDS_GTE2",
                i_CEB=0,
                i_I=clk100_pads.p,
                i_IB=clk100_pads.n,
                o_O=clk100_sig),
            Instance("BUFG", i_I=clk100_sig, o_O=clk100_buf),
        ]
        pcie_x1 = platform.request("pcie_x1")
        #serial = platform.request("serial")
        crg = _CRG(platform, sys_clk_freq, clk100_buf, ~pcie_x1.rst_n, None)
        self.submodules.crg = crg
        #self.specials += [
        #    Instance("BUFG", i_I=crg.cd_clk1.clk, o_O=serial.rx),
        #]
        #self.comb += serial.tx.eq(~pcie_x1.rst_n)
        self.comb += pcie_x1.clk_req_n.eq(0)
        self.submodules.uart_bridge = UARTWishboneBridge(platform.request("serial"), sys_clk_freq, baudrate=115200)
        self.add_wb_master(self.uart_bridge.wishbone)
        if hasattr(self, "cpu") and self.cpu.name == "vexriscv":
            self.register_mem("vexriscv_debug", 0xf00f0000, self.cpu.debug_bus, 0x100)

# Build --------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LiteX SoC on PicoEVB")
    builder_args(parser)
    args = parser.parse_args()

    soc = BaseSoC()
    builder = Builder(soc, **builder_argdict(args))
    builder.build()


if __name__ == "__main__":
    main()