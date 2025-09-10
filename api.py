import os
from flask import Flask, request, jsonify
from scrap import get_last_two_prices

app = Flask(__name__)

@app.route("/", methods=["GET"])
def uranium_price():
    # Read query parameters instead of JSON body
    job_run_id = request.args.get("id", "1")
    priceType = request.args.get("priceType", "spot")

    if priceType not in ["spot", "long-term"]:
        return jsonify({
            "jobRunID": job_run_id,
            "status": "errored",
            "error": "Invalid priceType. Must be 'spot' or 'long-term'."
        }), 400

    try:
        last_two = get_last_two_prices()
        print("Fetched Prices:", last_two)

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
    # Railway provides the port via env variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
