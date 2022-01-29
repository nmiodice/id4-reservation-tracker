# id4-reservation-tracker
A command line tool to check the status of a VW ID4 Reservation. Thank you to the kind folks at [vwidtalk](https://www.vwidtalk.com/threads/production-order-status-codes-find-what-is-happening-with-my-order.3292/) for providing a list of useful codes

## Requirements
- Docker

## Usage

```bash
export USERNAME=<email used for VW reservation>
export PASSWORD=<password used for VW reservation>

# optional - the default page load timeout is 10 seconds, which
# should be fine for most people. If your internet is slow, you
# can bump this up.
export PAGE_LOAD_TIMEOUT_SECONDS=20

./run.sh
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
```
