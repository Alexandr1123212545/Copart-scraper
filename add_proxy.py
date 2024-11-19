import argparse
from database.core import StorageHandler

def main():
    parser = argparse.ArgumentParser(description="Add proxy to DB")

    parser.add_argument(
        '--proxies',
        type=str,
        required=True,
        help='List of proxy in the format: [protocol://ip_1:port, protocol://ip_2:port]'
    )

    args = parser.parse_args()
    try:
        proxies = args.proxies.split(',')
        StorageHandler.set_proxy(proxies)
        print("Proxies added successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()