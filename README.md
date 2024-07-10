# wheres_Dmarc
The Wheres Dmarc Tool analyzes DMARC records for a list of domains. It extracts the main domain, checks for DMARC records, and interprets DMARC policies, providing insights into email authentication and domain security. 

Features

Extracts the main domain from a given URL.
Checks for the existence of DMARC records.
Interprets and prints the DMARC policy details.

Requirements

Python 3.x
dnspython library
tld library

      pip install dnspython tld

Usage

Prepare an input file with one domain per line. For example, domains.txt:

        example.com
        example.org
        example.net

Run the script from the command line:

        python wheres_dmarc.py <input_file>

Replace <input_file> with the path to your input file. For example:

        python wheres_dmarc.py domains.txt


