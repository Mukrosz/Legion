#!/usr/bin/python3
"""
Query Legion API for project info
"""

import argparse
import json
import jwt
import requests
from   datetime import datetime
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

if __name__ == '__main__':
    description = ("Scrape for Legion project(s) details\n")
    parser = argparse.ArgumentParser(description     = description,
                                     formatter_class = argparse.RawTextHelpFormatter
    )
    parser.add_argument('--filter','--f',
                         help     = 'Project name to filter',
                         default  = '',
                         required = False 
    )
    parser.add_argument('--view','--v',
                         help     = 'View all, new, old projects. Default all',
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
                         default  = 'https://api.legion.cc/rounds',
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
            projects += response.json()

        if args.short:
           summary = [ [p['project']['name'],
                        p['rounds'][0].get('chain', {}).get('name'),
                        p['rounds'][0].get('contract', {}).get('address', '')] for p in projects if args.filter in p['project']['name'].lower()
           ]
           summary = sorted(summary, key = lambda x: x[0].lower())
           print_tabular(summary, ['Name', 'Chain', 'Contract'])
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
