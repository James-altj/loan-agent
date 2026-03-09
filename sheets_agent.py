import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define API scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

# Authorize client
client = gspread.authorize(creds)

# Open spreadsheet
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