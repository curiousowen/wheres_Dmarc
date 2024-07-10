import dns.resolver
import sys
from tld import get_fld

def extract_main_domain(url):
    """Extracts the main domain from the provided URL."""
    return get_fld(url, fix_protocol=True)

def fetch_dmarc_record(domain):
    """Fetches the DMARC record for the provided domain."""
    try:
        query = f'_dmarc.{domain}'
        response = dns.resolver.resolve(query, 'TXT')
        for txt in response:
            if 'DMARC1' in str(txt):
                return str(txt)
        return None
    except dns.resolver.NXDOMAIN:
        return None
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.Timeout:
        return None
    except Exception:
        return None

def interpret_dmarc(domain, record):
    """Interprets and prints the DMARC policy from the provided record."""
    if record is None:
        print(f"{domain}:\t No DMARC record found")
        return

    segments = record.split(';')
    for segment in segments:
        segment = segment.strip().lower()
        if segment.startswith('p=none') or segment.startswith('sp=none'):
            print(f"{domain}:\t DMARC policy is 'none' (p=none or sp=none)")
            return
        if segment.startswith('pct='):
            try:
                percentage = int(segment.split('=')[1])
                if percentage < 100:
                    print(f"{domain}:\t DMARC percentage is less than 100% (pct={percentage})")
                    return
            except ValueError:
                pass
    print(f"{domain}:\t DMARC record is valid with full coverage")

def read_domains(file_path):
    """Reads domains from the input file and processes each."""
    try:
        with open(file_path, 'r') as file:
            domains = file.readlines()
            for line in domains:
                domain = line.strip()
                if domain:
                    main_domain = extract_main_domain(domain)
                    dmarc_record = fetch_dmarc_record(main_domain)
                    interpret_dmarc(domain, dmarc_record)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dmarc_checker.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    read_domains(input_file)
