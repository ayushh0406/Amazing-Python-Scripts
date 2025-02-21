from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_bmi(weight, height):
    height_in_meters = height / 100
    bmi = weight / (height_in_meters ** 2)
    return round(bmi, 2)

def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"])
            
            if weight <= 0 or height <= 0:
                raise ValueError("Height and weight must be positive values.")

            bmi = calculate_bmi(weight, height)
            interpretation = interpret_bmi(bmi)

            return render_template("result.html", bmi=bmi, interpretation=interpretation)
        except ValueError as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
