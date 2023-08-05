'''
    CLI entry point
'''
import click
import click_log
import logging
from ibcli.config_cli import config
#from ibcli.download_cli import download
from ibcli.reports_cli import reports

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

@click.group()
@click_log.simple_verbosity_option(logger)
def cli():
    ''' Interactive Brokecs CLI access to Flex Queries via Web Service '''
    pass

@click.command("bal")
@click_log.simple_verbosity_option(logger)
def balance():
    ''' Download the current account cash balance '''
    from ibcli.reports import Reports
    lines = Reports().balance()
    for line in lines:
        print(line)

@click.command("dl2")
@click.option("--id", type=int, required=True)
@click_log.simple_verbosity_option(logger)
def download2(id):
    ''' Download the report using ibflex '''
    from ibflex import client
    from ibcli.configuration import Config

    cfg = Config()
    token = str(cfg.token)
    id_str = str(id)

    result = client.download(token, id_str)
    print(result)

    # Use flexget script to download, for now.

    # Save
    #open()

@click.command("dl")
@click.option("--id", "-id", type=int, required=True)
@click.option('-t', '--token', type=str, help='IB authentication token', required=True)
@click_log.simple_verbosity_option(logger)
def download(id, token):
    ''' Download a report '''
    from ibcli.downloader import Downloader
    #from ibcli.configuration import ConfigReader
    from ibcli.helpers import save_report

    result = Downloader().get(id, token)
    #print(result)
    save_report("name", result)

@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

@click.command()
@click.option("--file", "-f", type=str, required=True, help='the name of the file to parse')
def parse(file):
    '''
    Parse the downloaded report. 
    Currently only for Cash Transactions. 
    '''
    from ibflex import parser
    import operator

    # FlexQueryResponse
    response = parser.parse(file)
    # print(response)

    statement = response.FlexStatements[0]
    # print(statement)

    txs_tuple = statement.CashTransactions
    txs = list(txs_tuple)
    # Sort by dateTime, symbol
    txs.sort(key=operator.attrgetter("dateTime", "symbol", "type.name"))
    
    for tx in txs:
        #print(tx.type.name)
        output = (f"{tx.dateTime.date()} {tx.type.name:15} {str(tx.listingExchange):6} " +
            f"{str(tx.symbol):5} {tx.amount:>7.2f} {tx.currency}")
        print(output)


##########################################
# Commands

cli.add_command(balance)
#cli.add_command(hello)
cli.add_command(download2)
cli.add_command(download)
cli.add_command(parse)

# Sub-commands

cli.add_command(config)
#cli.add_command(download)
cli.add_command(reports)
