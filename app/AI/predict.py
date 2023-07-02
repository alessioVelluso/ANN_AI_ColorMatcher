from AI.model2 import ANN, le, ct, np, ss
from PIL import ImageColor
from flask import jsonify

def predict_single(color):
    try:
        if len(color) < 7: color = color + "0"*(7-len(color))
        color = ImageColor.getcolor(color, "RGB") + (1,)
        color = np.array(color)
        print(color)

        #X_input = [[color]]
        #X_input =ct.transform(X_input).toarray()
        X_input = [color]
        X_input =ss.transform(X_input)
        print(X_input)
        
        predictions = ANN.predict(X_input)

        # Ottieni gli indici delle tre predizioni più alte
        top_indices = np.argsort(predictions[0])[-1:]

        # Ottieni le percentuali di accuratezza delle tre predizioni più alte
        top_probabilities = predictions[0][top_indices]

        col_result = le.inverse_transform(top_indices)[0]
        prob = top_probabilities[0]

        return jsonify({"color": col_result, "prob": str(prob) }), 200
    
    except Exception as e:
        err_obj = { 
            "message": "Something went wrong, look at the console for more info",
            "status": 500,
            "err": str(e)
        }
        return jsonify(err_obj), 500