from AI.model import ANN, le, ct, np, ss
import colorsys
from PIL import ImageColor
from flask import jsonify

def predict_single(color):
    try:
        if len(color) < 7: color = color + "0"*(7-len(color))
        rgb = ImageColor.getcolor(color, "RGB")
        hsl = colorsys.rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)

        color = np.array(hsl  + (1,))
        X_input = color.reshape(-1, 4)
        X_input[:, :-1] = ss.transform(X_input[:, :-1])
        X_input[:, -1] = [float(val) for val in X_input[:, -1]]
        
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