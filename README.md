# Description
The script scapes Legion's API for project information

Example:
```
Name          Chain  Contract Stage    Asset  FDV   Target  TGE         Vest  Cliff  Lock  Requested
------------  -----  -------- ------   -----  ----  ------  ----------  ----  -----  ----  ---------
project1      eth    0x2c...  open     USDC   220M  1M      Q4 2025     1095  365    0     1.2M         
project2      arb    0x4A...  closed   USDC   45M   500k    Q1/Q2 2025  730   182    0     500k         
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

```/legion.py --short --token 'long_bearer_token_string'```

> Display a summary for ongoing/upcoming projects

```/legion.py --short --view 'new' --token 'long_bearer_token_string'```

> Display a summary for a specific project

```/legion.py --short --filter 'project1' --token 'long_bearer_token_string'```

> Display a raw json for a specific project

```/legion.py --filter 'project1' --token 'long_bearer_token_string'```

## Help menu
> ./query_projects.py -h
```
usage: query_projects.py [-h] [--filter FILTER] [--view {all,new,old}] [--short] [--url URL] [--token TOKEN]

Scrape for Legion project details

options:
  -h, --help            show this help message and exit
  --filter FILTER, --f FILTER
                        Project name to filter
  --view {all,new,old}, --v {all,new,old}
                        View all, new, old projects. Default new
  --short, --s          Display condensed format, otherwise print raw json
  --url URL, --u URL    End-point URL
  --token TOKEN, --t TOKEN
                        Bearer token
```
