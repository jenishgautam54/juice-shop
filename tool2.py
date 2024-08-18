import requests
import argparse

# Expanded list of potential sensitive data exposure endpoints
potentialEndpoints = [
    "/rest/user/whoami",
    "/rest/admin/application-configuration",
    "/ftp",
    "/rest/admin/user",
    "/rest/admin/orders",
    "/api/v1/users",
    "/api/v1/auth/login",
    "/api/v1/auth/register",
    "/api/v1/payment",
    "/api/v1/account",
    "/api/v1/account/settings",
    "/api/v1/admin",
    "/api/v1/admin/settings",
    "/api/v1/admin/users",
    "/api/v1/admin/orders",
    "/api/v1/profile",
    "/api/v1/orders",
    "/api/v1/cart",
    "/api/v1/wishlist",
    "/api/v1/auth/refresh",
    "/api/v1/auth/logout",
    "/rest/products/search",
    "/rest/user/change-password",
    "/admin/config",
    "/admin/settings",
    "/admin/users",
    "/admin/orders",
    "/admin/inventory",
    "/admin/authenticate",
    "/admin/login",
    "/admin/logout",
    "/admin/refresh",
    "/admin/reset-password",
    "/admin/api-keys",
    "/admin/smtp-settings",
    "/api/v1/upload",
    "/api/v1/download",
    "/api/v1/notifications",
    "/api/v1/transactions",
    "/rest/system/status",
    "/rest/system/logs",
]

# Function to test for sensitive data exposure
def test_sensitive_data_exposure(base_url, potentialEndpoints):
    exposed_urls = []  # List to store URLs where data exposure is detected
    
    for endpoint in potentialEndpoints:
        url = base_url + endpoint
        try:
            # Send the request to the server
            response = requests.get(url)
            
            # Look for sensitive data patterns in the response
            if "password" in response.text or "key" in response.text or "token" in response.text:
                print(f"[+] Sensitive data exposure detected at {url}")
                exposed_urls.append(url)  # Add the URL to the list if sensitive data is detected
            else:
                print(f"[-] No sensitive data exposure at {url}")
        except Exception as e:
            print(f"Error testing {url}: {str(e)}")
    
    return exposed_urls  # Return the list of URLs where exposures were detected

# Main function to parse command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Sensitive Data Exposure Testing Tool")
    parser.add_argument("domain", help="The base URL of the website to test for sensitive data exposures")
    args = parser.parse_args()

    base_url = args.domain
    exposed_urls = test_sensitive_data_exposure(base_url, potentialEndpoints)

    # Print the list of URLs where data exposures were detected
    if exposed_urls:
        print("\n[!] Sensitive data exposures were detected at the following URLs:")
        for url in exposed_urls:
            print(f" - {url}")
    else:
        print("\n[+] No sensitive data exposures were detected.")

if __name__ == "__main__":
    main()