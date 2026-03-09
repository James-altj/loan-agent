from flask import Flask, request, jsonify
from datetime import datetime
from sheets_agent import save_to_sheet

app = Flask(__name__)

@app.route("/submit-form", methods=["POST"])
def submit_form():

    data = request.json

    form_data = {
        "timestamp": str(datetime.now()),
        "name": data["name"],
        "phone": data["phone"],
        "loan_type": data["loan_type"],
        "collateral": data["collateral"],
        "amount": data["amount"]
    }

    save_to_sheet(form_data)

    return jsonify({"message": "Application saved successfully"})


if __name__ == "__main__":
    app.run(debug=True)