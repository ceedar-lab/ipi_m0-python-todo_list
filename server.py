from flask import Flask, request, render_template

app = Flask(__name__)
app.debug = True

# @app.route("/", methods=['GET', 'POST'])
# def index():
#     if request.method == "POST":
#         name = request.form["name"]
#         return name + " Hello"
#     return render_template("index2.html")
    
# @app.route("/", methods=['GET', 'POST'])
# def index2():
#     if request.method == "POST":
#         name2 = request.form["name2"]
#         return name2 + " Hellooo"
#     return render_template("index2.html")
    
@app.route("/", methods=['GET', 'POST'])
def index2():
    if request.method == "POST":
        name = request.form["name"]
        return name + " Hello"        
    return render_template("index2.html")




if __name__ == "__main__":
    app.run()