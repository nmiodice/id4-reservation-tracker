import os
import chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import jwt
import requests
import json

KNOWN_VW_ORDER_CODES = {
    "03": "Locked",
    "10": "Locked next step request production",
    "15-1": "Vehicle Scheduled For Production (call your dealer now they usually have better dates than the portal.)",
    "15-2": "Vehicle in production",
    "20-1": "Production complete, VIN assigned",
    "20-2": "Left the port (at this point some dealers can tell you a ship number for those really obsessed with this.)",
    "30-1": "Arrived in port but not unloaded yet.",
    "30-2": "Unloaded from ship, not cleared customs yet.",
    "30-3": "Cleared customs, waiting to load on transporter",
    "35-1": "released to the transporter (rail)",
    "35-2": "released to the transporter (truck)",
    "35-3": "released to the transporter (shorter distance truck?)",
    "50": "and higher- Arriving at dealer",
}

GRAPHQL_API_ENDPOINT = "https://api.vw.com/graphql"


def makeGraphQLAPICall(s, authToken, body):
    headers = {
        "authorization": "Bearer " + authToken,
        "content-type": "application/json; charset=utf-8",
    }

    response = s.post(GRAPHQL_API_ENDPOINT, headers=headers, json=body, verify=False)
    return json.loads(response.text)


def main():
    user = os.getenv("USERNAME")
    passwd = os.getenv("PASSWORD")

    with webdriver.Chrome(options=chrome.options()) as driver:
        print("Loading VW reservation page...")
        driver.get("https://www.vw.com/myVW/myreservations/active")

        # enter username
        print("Entering username...")
        usernameInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input_email"))
        )
        usernameInput.send_keys(user)

        # submit username
        print("Submitting username...")
        nextButton = driver.find_element(By.XPATH, "//button[@id='next-btn']")
        nextButton.click()

        # enter password
        print("Entering password...")
        passwordInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        passwordInput.send_keys(passwd)

        # submit password
        print("Submitting password...")
        nextButton = driver.find_element(By.XPATH, "//button[@id='next-btn']")
        nextButton.click()

        # wait for load
        print("Waiting for reservation page to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[text() = 'Reservation ID']")
            )
        )

        # get auth token for VW Graph API
        print("Parsing authentication token...")
        authToken = driver.get_cookie("azt")["value"]

        print("Parsing authentication subject...")
        oAuthSubject = jwt.decode(authToken, options={"verify_signature": False})["sub"]

        print("Parsing reservation id...")
        reservationID = driver.get_cookie("selectedReservation")["value"]

        s = requests.session()
        s.cookies.update({c["name"]: c["value"] for c in driver.get_cookies()})

        print("Making GraphQL API: GetUserProfileByUserId")
        response = makeGraphQLAPICall(
            s,
            authToken,
            {
                "operationName": "GetReservationDealerDetails",
                "variables": {},
                "query": 'query GetReservationDealerDetails {\n  authenticatedGetReservation(publicId: "__RESERVATION_ID__") {\n    deliveryDealerCode\n    orderStatusCode\n    publicReservationId\n    reservationStatus\n    estimatedProductionDate\n    configurationId\n    vwModelCodeKey\n    marketingCode\n    fromEstmtdDlvryDate\n    toEstmtdDlvryDate\n    __typename\n  }\n  getDealerById(id: "__DEALER_ID__") {\n    name\n    address {\n      address1\n      address2\n      city\n      state\n      zip\n      __typename\n    }\n    __typename\n  }\n}\n'.replace(
                    "__RESERVATION_ID__", reservationID
                ),
            },
        )

        print("Parsing GraphQL API response")
        print()

        usefulData = response["data"]["authenticatedGetReservation"]
        orderCode = usefulData["orderStatusCode"]

        if orderCode in KNOWN_VW_ORDER_CODES:
            status = orderCode + " (" + KNOWN_VW_ORDER_CODES[orderCode] + ")"
        else:
            status = orderCode + "(???)"

        print("Order Status".ljust(40), end="")
        print(status)

        print("Estimated Production Date".ljust(40), end="")
        print(usefulData["estimatedProductionDate"])

        print("Estimated Deliver Date (beginning)".ljust(40), end="")
        print(usefulData["fromEstmtdDlvryDate"])

        print("Estimated Deliver Date (end)".ljust(40), end="")
        print(usefulData["toEstmtdDlvryDate"])


if __name__ == "__main__":
    main()
