# id4-reservation-tracker
A command line tool to check the status of a VW ID4 Reservation

## Requirements
- Docker

## Usage

```bash
export USERNAME=<email used for VW reservation>
export PASSWORD=<password used for VW reservation>

./run.sh
```

## Sample Output

```bash
$ ./run.sh
Loading VW reservation page...
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

Order Status                        -->  03 (Locked)
Estimated Production Date           -->  None
Estimated Deliver Date (beginning)  -->  2022-4-01
Estimated Deliver Date (end)        -->  2022-5-01
```
