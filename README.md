# Description
The script scapes Legion's API for project information

Example:
```
Name         Curator   Chain  Contract Stage    Asset  FDV   Target  TGE         Vest  Cliff  Lock  Requested
--------     -------   -----  -------- ------   -----  ----  ------  ----------  ----  -----  ----  ---------
project1     legion    eth    0x2c...  open     USDC   220M  1M      Q4 2025     1095  365    0     1.2M         
project2     nozomi    arb    0x4A...  closed   USDC   45M   500k    Q1 2025     0     182    0     500k         
project3     cookie    eth    0x4A...  closed   USDC   100M  2M      Q3 2025     730   182    0     1M         
```
# Requirements
##  Python
> Python 3.11.2 (may work with older versions)
##  Legion bearer token
A bearer token `--t` is required to pull information. Follow steps below to retrieve it from your authenticated Chrome session
Using Chrome
- Login to Legion.cc
- Open Developer tools (Ctrl + Shift + I)
- Refresh Legion page and select _Network_ tab
- Select _Filter_ icon:
  - type `round`
  - select _Fetch/XHR_
- Select any of the `rounds` results and then select _Headers_ tab
- Look for _Authorizations_. That's your Bearer token (very long string)

# Usage
> Display a summary for all projects

```./query_projects.py --short --token 'long_bearer_token_string'```

> Feed token string from a file

```./query_projects.py --short --token $(cat token.txt)```

> Display a summary for projects from cookie and nozomi curators
```./query_projects.py --token $(cat ../token.txt) --s --c 'cookie, nozomi'```

> Display a summary for ongoing and upcoming projects

```./query_projects.py --short --view 'new' --token 'long_bearer_token_string'```

> Display a summary for a specific project

```./query_projects.py --short --filter 'project1' --token 'long_bearer_token_string'```

> Display a raw json for a specific project

```./query_projects.py --filter 'project1' --token 'long_bearer_token_string'```

## Help menu
> ./query_projects.py -h
```
usage: query_projects.py [-h] [--filter FILTER] [--view {all,new,old}] [--curators CURATORS] [--short] [--url URL] [--token TOKEN]

Scrape for Legion project details

options:
  -h, --help            show this help message and exit
  --filter FILTER, --f FILTER
                        Project name to filter
  --view {all,new,old}, --v {all,new,old}
                        View all, new, old projects. Default new
  --curators CURATORS, --c CURATORS
                        Specify curators (comma separated). Default: legion, cookie, nozomi
  --short, --s          Display condensed format, otherwise print raw json
  --url URL, --u URL    End-point URL
  --token TOKEN, --t TOKEN
                        Bearer token
```
