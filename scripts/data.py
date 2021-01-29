import warnings
from dataclasses import dataclass
from brownie import interface
from brownie.network.contract import InterfaceContainer
from rich.console import Console
import logging
from rich.logging import RichHandler
from prometheus_client import Gauge, start_http_server

warnings.simplefilter( "ignore" )

console = Console()
logging.basicConfig( level="ERROR", format="%(message)s", datefmt="[%X]",
                     handlers=[RichHandler( rich_tracebacks=True )] )
log = logging.getLogger( "rich" )

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@dataclass
class Sett:
    name: str
    sett: InterfaceContainer

    def describe(self):
        scale = 10 ** self.sett.decimals()
        try:
            info = {
                    "pricePerShare": self.sett.getPricePerFullShare() / scale,
                    "totalSupply"  : self.sett.totalSupply() / scale
                    }
        except ValueError as e:
            info = {}
            log.exception( str( e ) )

        return info


setts = {
        "badger"       : "0x19D97D8fA813EE2f51aD4B4e04EA08bAf4DFfC28",
        "renCrv"       : "0x6dEf55d2e18486B9dDfaA075bc4e4EE0B28c1545",
        "sbtcCrv"      : "0xd04c48A53c111300aD41190D63681ed3dAd998eC",
        "tbtcCrv"      : "0xb9D076fDe463dbc9f915E5392F807315Bf940334",
        "uniBadgerWbtc": "0x235c9e24D3FB2FAFd58a2E49D454Fdcd2DBf7FF1",
        "harvest"      : "0xAf5A1DECfa95BAF63E0084a35c62592B774A2A87",
        "digg"         : "0x7e7E112A68d8D2E221E11047a72fFC1065c38e1a",
        "uniDiggWbtc"  : "0xC17078FDd324CC473F8175Dc5290fae5f2E84714",
        "sushiDiggWbtc": "0x88128580ACdD9c04Ce47AFcE196875747bF2A9f6"
        }


def get_data():
    return [Sett( name=f'Sett_{name}', sett=interface.Sett( sett ) ) for name, sett in setts.items()]


if __name__ == '__main__':
    for s in [Sett( name=f'Sett_{name}', sett=interface.Sett( sett ) ) for name, sett in setts.items()]:
        info = s.describe()
        console.rule( title=s.name )
        for key, value in info.items():
            console.print( f'[blue]{key} : [red] {value}' )
