# id4-reservation-tracker
A command line tool to check the status of a VW ID4 Reservation. Thank you to the kind folks at [vwidtalk](https://www.vwidtalk.com/threads/production-order-status-codes-find-what-is-happening-with-my-order.3292/) for providing a list of useful codes

## Requirements
- Docker (Unix)
  - https://docs.docker.com/engine/install/ubuntu/
- Docker Desktop (Windows) 
  - https://docs.docker.com/desktop/windows/install/

## Setup
1. Clone or download this repository
2. Create a file called **.env.template** in the main directory
3. Copy the contents below into that file, setting your username and password for the VW reservation portal.
```
USERNAME=<Your Username Here>
PASSWORD=<Your Password Here>

# optional
PAGE_LOAD_TIMEOUT_SECONDS=
VERBOSE=1 
```

## Optional settings
- In the supplied .env file
  - Provide a value for **PAGE_LOAD_TIMEOUT_SECONDS** to override the default 20 second timeout.
  ```
  PAGE_LOAD_TIMEOUT_SECONDS=60
  ```
  - Change the value of **VERBOSE** to 1 to get the raw response body from VW's reservation system
  ```
  VERBOSE=1
  ...
  Raw response data
  {'data': {'authenticatedGetReservation': {'deliveryDealerCode': '1234', 'orderStatusCode': '<See link to vwidtalk forums above for list of expected status codes>', 'publicReservationId': 'ABC123', 'reservationStatus': 'ACTIVE',  'estimatedProductionDate': None, 'configurationId': 'AAAAAAAAAAAAAAAAAAA-BBBBBBBBBBBBBBBBBBBBB-CCCCCCCCCCCC', 'vwModelCodeKey': '1239040', 'marketingCode': None, 'fromEstmtdDlvryDate': 'YYYY-MM-DD', 'toEstmtdDlvryDate': 'YYYY-MM-DD', 'vin': 'ABC!@#', '__typename': 'Reservation'}, 'getDealerById': None}}
  ```

## Usage (Unix)

```bash
./run.sh
```

## Usage (Windows)
```
./run.ps1
```

## Sample Output

```bash
$ ./run.sh
Entering username...
Submitting username...
Entering password...
Submitting password...
Waiting for reservation page to load...
Parsing authentication token...
Parsing authentication subject...
Parsing reservation id...
Making GraphQL API: GetUserProfileByUserId
Parsing GraphQL API response

Order Status                            03 (Locked)
Estimated Production Date               None
Estimated Deliver Date (beginning)      2022-4-01
Estimated Deliver Date (end)            2022-5-01
VIN                                     None
Press any key to close ...
```
