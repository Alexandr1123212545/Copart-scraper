# Parser for copart

## This is an asynchronous parser for a site selling auto from the USA.

### Properties
- Collects, stores and updates basic data about lots.
- Has its own database.
- Has a high speed of information collection due to the use of several proxies.
- Can work both on a remote server using a pool of third-party addresses and locally - using the address of the local machine.
- Can be used in other projects as an independent microservice.
- The speed of work depends on the size of the proxy pool.
- It is not recommended to run a project without using an address pool more than once every 30 minutes.
- The project only works on Linux.

## Installing
1. Clone the repository:
    ```bash
    https://github.com/Alexandr1123212545/Copart-scraper.git
    ```
2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Edit the ***.env*** file
   BASE_URL=https://www.copart.com
   SALES_LIST=https://www.copart.com/public/lots/search-results/all
   SALES_PAGE=https://www.copart.com/public/salesListResultPage

   DB_HOST=host
   DB_PORT=port
   DB_USER=name_your_data_base
   DB_PASS=password_your_data_base
   DB_NAME=name_your_data_base

5. I recommend adding a proxy
   1. Go to the root directory
   2. Enter the command in the terminal
      ```bash
      python add_proxy.py --proxies "protocol://ip-address_1:port, protocol://ip-address_2:port"
      ```

## Usage
   While in the root directory, enter the command:
   ```bash
   python main.py
   ```