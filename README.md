# id4-reservation-tracker
A command line tool to check the status of a VW ID4 Reservation. Thank you to the kind folks at [vwidtalk](https://www.vwidtalk.com/threads/production-order-status-codes-find-what-is-happening-with-my-order.3292/) for providing a list of useful codes

## Requirements
- Docker (Unix)
  - https://docs.docker.com/engine/install/ubuntu/
- Docker Desktop (Windows) 
  - https://docs.docker.com/desktop/windows/install/

## Setup
- Clone or download this repository
- Review the contents of `.env.template` and configure your environment correctly. At a minimum, you will need to set environment variables for `USERNAME` and `PASSWORD`.
  - On `*nix` systems, you can run:
    ```bash
    $ cp .env.template .env
    
    # configure variables here
    $ vim .env
    
    $ . .env
    ```
  - On `*nix` systems, you could also use https://direnv.net/
  - On windows, these can be set in Powershell using `$Env:<variable-name> = "<new-value>"`

## Optional settings
  - Provide a value for **PAGE_LOAD_TIMEOUT_SECONDS** to override the default 20 second timeout.
  ```
  PAGE_LOAD_TIMEOUT_SECONDS=60
  ```
  - Change the value of **VERBOSE** to 1 to get the raw response body from VW's reservation system
  ```
  VERBOSE=1
  ...
  Raw response data
  {
    "data": {
      "authenticatedGetReservation": {
        "__typename": "Reservation",
        "configurationId": "...",
        "deliveryDealerCode": "...",
        "estimatedProductionDate": "...",
        "fromEstmtdDlvryDate": "...",
        "marketingCode": "...",
        "orderStatusCode": "<See link to vwidtalk forums above for list of expected status codes>",
        "publicReservationId": "...",
        "reservationStatus": "ACTIVE",
        "toEstmtdDlvryDate": "...",
        "vin": "...",
        "vwModelCodeKey": "..."
      },
      "getDealerById": null
    }
  }
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
