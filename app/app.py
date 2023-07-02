from flask import Flask, jsonify, request, render_template
import atexit, os

from AI.predict import predict_single

app = Flask(__name__)

dailyData = []
def write_in_file():
    for obj in dailyData:
        bg = obj["bg_color"]
        front = obj["front_color"]
        match = obj["match"]
        with open("./app/AI/data.csv", 'a', encoding='utf8') as f:
            f.write(f"\n{bg},{front},{match}")

    print("Data saved, closing the server.")




@app.route('/')
def index():
    return render_template('index.html')



@app.route('/api/send_result', methods=['POST'])
def send_result():
    try:
        obj = request.json
        dailyData.append(obj)
        return jsonify({"message": "OK", "status": 200}), 200
    
    except Exception as e:
        err_obj = { 
            "message": "Something went wrong, look at the console for more info",
            "status": 500,
            "err": str(e)
        }
        return jsonify(err_obj), 500
    

@app.route('/api/predict_single/<color>', methods=['GET'])
def api_predict_single(color):
    color = '#'+color
    print(color)
    return predict_single(color)







atexit.register(write_in_file)
app.run(port=3000)