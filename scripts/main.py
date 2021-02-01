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
wbtc = interface.ERC20( '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599' )
tree = interface.Tree( tree )

sushi = interface.Pair('0x9a13867048e01c663ce8Ce2fE0cDAE69Ff9F35E3')
uni = interface.Pair('0xe86204c4eddd2f70ee00ead6805f917671f56c52')


def main():
    sett_gauge = Gauge( "sett", "", ["sett", "param"] )
    treasury_gauge = Gauge( "treasury", '', ['token', 'param'] )
    rewards_gauge = Gauge( 'rewards', '', ['token'] )
    digg_gauge = Gauge( 'digg_price', '', ['value'] )

    start_http_server( 8801 )

    setts = scripts.data.get_sett_data()
    treasury = scripts.data.get_treasury_data()
    digg_prices = scripts.data.get_digg_data()

    for block in chain.new_blocks( height_buffer=20 ):

        console.rule( title=f'[green]{block.number}' )
        console.print( f'Calculating reward holdings..' )

        badger_rewards = badger.balanceOf( tree.address ) / 1e18
        digg_rewards = digg.balanceOf( tree.address ) / 1e9
        rewards_gauge.labels( 'badger' ).set( badger_rewards )
        rewards_gauge.labels( 'digg' ).set( digg_rewards )

        for sett in setts:
            info = sett.describe()
            console.print( f'Processing [bold]{sett.name}...' )
            for param, value in info.items():
                sett_gauge.labels( sett.name, param ).set( value )

        for token in treasury:
            info = token.describe()
            console.print( f'Processing [bold]{token.name}...' )
            for param, value in info.items():
                treasury_gauge.labels( token.name, param ).set( value )
        price = digg_prices.describe()

        for param, value in price.items():
            console.print( f'Processing digg [bold]{param}...' )
            digg_gauge.labels( param ).set( value )

        digg_sushi_price = (sushi.getReserves()[0] / 1e8) / (sushi.getReserves()[1] / 1e9)
        digg_uni_price = (uni.getReserves()[0] / 1e8) / (uni.getReserves()[1] / 1e9)

        digg_gauge.labels( 'sushiswap' ).set(digg_sushi_price)
        digg_gauge.labels('uniswap').set(digg_uni_price)

