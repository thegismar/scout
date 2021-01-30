from rich.console import Console
from prometheus_client import Gauge, start_http_server
import warnings
import scripts.data
from brownie import chain
from brownie import interface

warnings.simplefilter( "ignore" )
console = Console()

tokens = {
        "badger": "0x3472A5A71965499acd81997a54BBA8D852C6E53d", "digg": "0x798D1bE841a82a273720CE31c822C61a67a601C3"
        }

tree = '0x660802Fc641b154aBA66a62137e71f331B6d787A'

badger = interface.Badger( tokens['badger'] )
digg = interface.Digg( tokens['digg'] )
tree = interface.Tree( tree )


def main():
    data_gauge = Gauge( "sett", "", ["sett", "param"] )
    rewards_gauge = Gauge( 'rewards', '', ['token'] )
    start_http_server( 8801 )
    setts = scripts.data.get_data()
    for block in chain.new_blocks():
        console.rule( title=f'[green]{block.number}' )
        badger_rewards = badger.balanceOf( tree.address ) / 1e18
        digg_rewards = digg.balanceOf( tree.address ) / 1e9
        rewards_gauge.labels( 'badger' ).set( badger_rewards )
        rewards_gauge.labels( 'digg' ).set( digg_rewards )
        for sett in setts:
            info = sett.describe()
            console.print( f'Processing [bold]{sett.name}...' )
            for param, value in info.items():
                data_gauge.labels( sett.name, param ).set( value )
