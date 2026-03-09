import os
import json
import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Read the environment variable
creds_json = os.environ.get("GOOGLE_CREDENTIALS")
if not creds_json:
    raise ValueError("GOOGLE_CREDENTIALS env variable not set")

creds_info = json.loads(creds_json)

# Fix the private_key newlines
creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")

creds = Credentials.from_service_account_info(creds_info, scopes=scope)

client = gspread.authorize(creds)
sheet = client.open("LoanApplications").sheet1


def process_form(data):

    amount = int(data["amount"])
    collateral = data["collateral"].lower()

    if collateral == "motorbike":
        category = "Motorbike Loan"
    elif collateral == "cereals":
        category = "Agricultural Loan"
    elif collateral == "land":
        category = "Land Loan"
    else:
        category = "Other"

    if amount > 500000:
        status = "Requires Approval"
    else:
        status = "Standard Review"

    return category, status


def save_to_sheet(data):

    category, status = process_form(data)

    row = [
        data["timestamp"],
        data["name"],
        data["phone"],
        data["loan_type"],
        data["collateral"],
        data["amount"],
        category,
        status
    ]

    sheet.append_row(row)