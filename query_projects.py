#!/usr/bin/python3
"""
Query Legion API for project info
"""

import argparse
import json
import jwt
import requests
from   datetime import datetime, timedelta
from   requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

def print_tabular(rows,headers = None):
    """ 
    Formats columns in tabularized format 

    :param  list rows    : list of lists
    :param  list headers : list of headers to print

    :return list         : list of lines to print
    """
    # in-between column space padding
    col_pad = 2

    # number of columns
    cols = len(rows[0])

    # list of each column's maximum width
    col_widths = [ max(len(row[column]) + col_pad for row in rows) for column in range(cols) ]

    # insert headers to the rows list
    if headers:
        # adjust items in col_widths (i.e '----') to match header length if data in column is shorter
        for i in range(len(col_widths)):
            if col_widths[i] - col_pad < len(headers[i]):
                col_widths[i] = len(headers[i]) + col_pad

        headers = [ ['-' * (item - col_pad) for item in col_widths],headers ]
        for header in headers: rows.insert(0,header)

    lines = []
    for row in rows:
        line = ''
        for i, item in enumerate(row):
            line = line + item.ljust(col_widths[i])
        print(line)
    print()

def shorten_number(num):
    """ 
    Reduce a large number into an abbreviated format(1000 -> 1k) 

    :param  int num : number to shorten 
    :return str     : shortened numer as a string
    """
    if num < 100:
        return ''
    for factor, suffix in [(1_000_000, 'M'), (1_000, 'k')]:
        if num >= factor:
            short = num / factor
            return f"{short:.1f}".rstrip('0').rstrip('.') + suffix
    return str(num)

def get_project_info(projects):
    """ 
    Extract relevant project fields and return a clean list of projects

    :param  json projects : a json of projects and assossiated values
    :return list          : a list of lists of projects and respective project values
    """
    project_list = []
    for project in projects:
        for tier in project.get('rounds'):
            name      = project['project']['name'].lower()
            chain     = tier.get('chain', {}).get('name', '')[:3].lower()
            contract  = tier.get('contract', {}).get('address', '')

            stage     = tier.get('stage', '').lower()
            stage     = 'closed' if 'success' in stage else stage

            asset     = tier.get('acceptedAsset', {}).get('symbol', '')
            fdv       = shorten_number(tier.get('raiseValuation', 0))
            target    = shorten_number(tier.get('raiseTarget', 0))
            tge       = str(tier.get('estimatedTge', ''))
            vesting   = str(timedelta(seconds = tier.get('vestingDuration', 0)).days)
            cliff     = str(timedelta(seconds = tier.get('vestingCliffDuration', 0)).days)
            lock      = str(timedelta(seconds = tier.get('lockupPeriod', 0)).days)
            requested = shorten_number(tier.get('totalRequestedAllocation', 0))

            project_list += [[ name, chain, contract, stage, asset, fdv, target, tge, vesting, cliff, lock, requested ]]

    return project_list

if __name__ == '__main__':
    description = ("Scrape for Legion project details\n")
    parser = argparse.ArgumentParser(description     = description,
                                     formatter_class = argparse.RawTextHelpFormatter
    )
    parser.add_argument('--filter','--f',
                         help     = 'Project name to filter',
                         default  = '',
                         required = False 
    )
    parser.add_argument('--view','--v',
                         help     = 'View all, new, old projects. Default new',
                         choices  = ['all', 'new', 'old'],
                         default  = 'all',
                         required = False 
    )
    parser.add_argument('--short', '--s',
                         help     = 'Display condensed format, otherwise print raw json',
                         action   = 'store_true',
                         default  = False,
                         required = False
    )
    parser.add_argument('--url', '--u',
                         help     = 'End-point URL',
                         default  = "https://api.legion.cc/rounds",
                         required = False
    )
    parser.add_argument('--token', '--t',
                         help    = 'Bearer token',
                         type    = str,
                         default = "",
                         required = False
    )

    args = parser.parse_args()

    decoded     = jwt.decode(args.token, options={"verify_signature": False})
    expiry_time = datetime.utcfromtimestamp(decoded.get("exp"))
    print("Your Bearer token expires at:", expiry_time.strftime('%Y-%m-%d %H:%M:%S UTC'))

    # essential headers
    headers = {
        "Authorization": "Bearer {}".format(args.token),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    try:
        # determine the view style 
        urls = [args.url + '?open=true', args.url + '?open=false']
        if args.view == 'old':
            urls = [args.url + '?open=false']
        elif args.view == 'new':
            urls = [args.url + '?open=true']

        projects = []
        for url in urls:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            project = response.json()
            projects += response.json()
        
        if args.short:
            projects = get_project_info(projects)
            summary = [ p for p in projects if args.filter in p[0].lower() ]
            summary = sorted(summary, key = lambda x: x[0].lower())
            print_tabular(summary, ['Name', 'Chain', 'Contract', 'Stage', 'Asset', 'FDV', 'Target', 'TGE', 'Vest', 'Cliff', 'Lock', 'Requested'])
        else:
            for p in projects:
                if args.filter in p.get("project", {}).get("name").lower():
                    print(json.dumps(p, indent = 4))
                    break

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Handle specific HTTP errors
    except ConnectionError as conn_err:
        print(f'Connection error occurred: {conn_err}')  # Handle network errors
    except Timeout as timeout_err:
        print(f'Timeout error occurred: {timeout_err}')  # Handle timeout errors
    except RequestException as req_err:
        print(f'Request error occurred: {req_err}')  # Handle other request errors
    except Exception as err:
        print(f'An error occurred: {err}')  # Handle any other exceptions
