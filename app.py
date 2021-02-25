from flask import Flask, render_template, request, jsonify
import random
from credit import Brand, CreditNumber, generate, validate

app = Flask(__name__)

amex = Brand("American Express", [15], ["34", "37"])
masterc = Brand("Master Card", [16], [str(number) for number in range(51, 56)])
visa = Brand("VISA", [13, 16, 19], [str(number) for number in range(40, 50)])

BRANDS = [amex, masterc, visa]


@app.route("/")
def home():
    brands_dict = {}
    for brand in BRANDS:
        numbers = []
        for i in range(3):
            numbers.append(generate(brand))
        brands_dict[brand.name] = numbers
            
    return render_template("home.html", brands=BRANDS, brands_dict=brands_dict)

@app.route("/generate", methods=["POST"])
def generator():
    picked_brand = request.form["brand"]
    for brand in BRANDS:
        if brand.name == picked_brand:
            number = generate(brand)
            break
    else:
        number = generate(random.choice(BRANDS))
    return jsonify({"number": f"Generated Number: {number}"})

@app.route("/validate", methods=["POST"])
def validator():
    message = validate(request.form.get("number"), BRANDS)
    return jsonify({"message": message})

@app.route("/advanced/")
def advanced():
    return render_template("adv_generator.html", brands=BRANDS)

@app.route("/adv_generator", methods=["POST"])
def advanced_generator():
    picked_brand = request.form["brand"]
    data_format = request.form["data_format"]
    count = request.form["count"]

    for brand in BRANDS:
        if brand.name == picked_brand:
            picked_brand = brand
            break

    makefile = makeFile(picked_brand, int(count))
    if data_format == "CSV":
        file = makefile.CSV()
    elif data_format == "XML":
        file = makefile.XML()
    else:
        file = makefile.JSON()
        
    return jsonify({"file": file, "data_format": data_format})


@app.route("/about/")
def about():
    return render_template("about.html")


class makeFile:
    def __init__(self, brand, count):
        self.brand = brand
        self.count = count

    def JSON(self):
        json = []
        for _ in range(self.count):
            creditcard = {
                "CreditCard": {
                    "Brand": self.brand.name,
                    "Number": generate(self.brand)
                }
            }
            json.append(creditcard)
        return json

    def CSV(self):
        data = []
        line = ",".join(["Brand", "Number"])
        data.append(line)

        for _ in range(self.count):
            line = ",".join([self.brand.name, generate(self.brand)])
            data.append(line)
        return "\n".join(data)

    def XML(self):
        xml = []
        line = "<root>\n"
        xml.append(line)
        
        for _ in range(self.count):
            line = f"  <CreditCard>\n    <Brand>{self.brand.name}</Brand>\n\
    <Number>{generate(self.brand)}</Number>\n  </CreditCard>\n"
            xml.append(line)
        xml.append("</root>")
        return "".join(xml)
        

if __name__ == "__main__":
    app.run(debug=True)