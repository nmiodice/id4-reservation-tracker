# id4-reservation-tracker
A command line tool to check the status of a VW ID4 Reservation. Thank you to the kind folks at [vwidtalk](https://www.vwidtalk.com/threads/production-order-status-codes-find-what-is-happening-with-my-order.3292/) for providing a list of useful codes

## Requirements
- Docker (Unix)
- https://docs.docker.com/engine/install/ubuntu/
- OR Docker Desktop (Windows) 
- https://docs.docker.com/desktop/windows/install/

## Setup
Edit the .env file to set your username and password environment variables.
These are copied into the docker container which is deleted after it runs.
```
export USERNAME=<email used for VW reservation UI>
export PASSWORD=<password used for VW reservation UI>
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
