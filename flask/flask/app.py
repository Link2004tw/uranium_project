from flask import Flask, request, jsonify
from scrap import get_last_two_prices

app = Flask(__name__)

@app.route("/", methods=["POST"])
def uranium_price():
    job_run_id = request.json.get("id", "1")
    priceType = request.json.get("data", {}).get("priceType", "spot")
    if priceType not in ["spot", "long-term"]:
        return jsonify({
            "jobRunID": job_run_id,
            "status": "errored",
            "error": "Invalid priceType. Must be 'spot' or 'long-term'."
        }), 400

    try:
        last_two = get_last_two_prices()
        print(last_two)
        if priceType == "long-term":
            date, price = last_two[1]  # second last price
        else:
            date, price = last_two[0]  # latest price
        return jsonify({
            "jobRunID": job_run_id,
            "data": {"uranium_price": price, "date": date},
            "result": price,
            "statusCode": 200
        })
    except Exception as e:
        return jsonify({
            "jobRunID": job_run_id,
            "status": "errored",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(port=8080)
