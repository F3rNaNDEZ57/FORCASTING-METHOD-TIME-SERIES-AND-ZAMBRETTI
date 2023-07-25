from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/forecast', methods=['GET'])
def get_forecast():
    # Here would be your forecast calculation, for simplicity let's say it returns "Fine weather"
    pressure_trend = forecast['trend'].values[-1]
    pressure_forecast = forecast['yhat1'].values[-1]
    is_northern_hemisphere = True  # Sri Lanka is in the Northern Hemisphere
    zambretti_forecast = zambretti(pressure_forecast, pressure_trend, is_northern_hemisphere)

    return jsonify({"forecast": zambretti_forecast})

if __name__ == "__main__":
    app.run(debug=True, port=5000) # runs the application
