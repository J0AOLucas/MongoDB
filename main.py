from flask import Flask, render_template
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017')
db = client['watches']

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    collection = db['products']
    documentos = collection.find().limit(5)
    
    return render_template("home.html", documentos=documentos)

@app.route("/produtos.html", methods=['GET'])
def produtos():
    collection = db['products']
    documentos = collection.find().limit(80)
    
    return render_template("produtos.html", documentos=documentos)


@app.route("/adicionar.html")
def adicionar():
    return render_template("adicionar.html")

@app.route("/produto.html/<id>", methods=['GET'])
def produto(id):
    collection = db['products']
    documentos = collection.find_one({'_id': ObjectId(id)})
    
    return render_template("produto.html", documentos=documentos)



if __name__ == "__main__":
    app.run(debug=True)
    