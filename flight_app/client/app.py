from flask import Flask, render_template, request
import requests
from requests.exceptions import RequestException

app = Flask(__name__)
API_URL = 'http://localhost:5000'

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    prediction = None
    selected_airport = None
    airports = []

    # Get airports list
    try:
        response = requests.get(f'{API_URL}/airports')
        airports = response.json()
    except RequestException as e:
        error = f"Could not fetch airports list: {str(e)}"
        return render_template('index.html', error=error)
    
    if request.method == 'POST':
        try:
            day_of_week = int(request.form['day_of_week'])
            airport_id = int(request.form['airport'])
            
            # Get prediction from API
            response = requests.post(
                f'{API_URL}/predict', 
                json={
                    'dayOfWeek': day_of_week, 
                    'airportId': airport_id
                }
            )
            
            if response.status_code == 200:
                prediction = response.json()['probability'] * 100
                selected_airport = next(
                    (a['DestAirportName'] for a in airports 
                     if a['DestAirportID'] == airport_id),
                    'Unknown Airport'
                )
            else:
                error = f"API Error: {response.text}"
        except RequestException as e:
            error = f"Could not connect to prediction service: {str(e)}"
        except (ValueError, KeyError) as e:
            error = f"Invalid input or response format: {str(e)}"
    
    return render_template('index.html', 
                         airports=airports,
                         prediction=prediction,
                         selected_airport=selected_airport,
                         error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)