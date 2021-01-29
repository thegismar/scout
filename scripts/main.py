from rich.console import Console
from prometheus_client import Gauge, start_http_server
import warnings
import scripts.data
from brownie import chain

warnings.simplefilter( "ignore" )
console = Console()


def main():
    data_gauge = Gauge( "badger_contract", "", ["contract", "param"] )
    timing = Gauge("badger_timing", "", ["vault", "action"])
    start_http_server( 8801 )
    contracts = scripts.data.get_data()
    for block in chain.new_blocks():
        console.rule( title=f'[green]{block.number}' )
        for contract in contracts:
            with timing.labels(contract.name, "describe").time():
                info = contract.describe()
                console.print( f'[bold]{contract.name}' )
                for param, value in info.items():
                    console.print(f'[green]{param} : [red] {value}')
                    data_gauge.labels( contract.name, param ).set( value )
