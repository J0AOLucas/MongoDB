from flask import Flask, request, redirect , url_for, render_template
from pymongo import MongoClient
from bson import ObjectId
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['watches']
collection = db['products']

@app.route("/", methods=['GET'])
def home():
    documentos = collection.find().limit(5)
    return render_template("home.html", documentos=documentos)


@app.route("/produtos.html", methods=['GET'])
def produtos():
    documentos = collection.find().limit(80)
    return render_template("produtos.html", documentos=documentos)


@app.route("/adicionar.html", methods=['GET', 'POST'])
def adicionar():
    if request.method == "GET":
        return render_template("adicionar.html")
    else: 
        Name = request.form['nome']
        Company = request.form['marca']
        Category = request.form['categoria']
        Price = request.form['preco']
        Localizacao = request.form['localizacao']
        Imagem = request.form['imagem']
        Observations = request.form['obs']
    
        new_acessory ={
            "Name" : Name,
            "Company" : {
                "Name" : Company} ,
            "Category" : Category,
            "Price" : Price,
            "Body" : {
                "Location" : Localizacao} ,
            "Imagem" : Imagem,
            "Observations" : Observations
        }
        
        db.products.insert_one(new_acessory)
        logging.info(f"Produto inserido com sucesso: {new_acessory}")
        
        return redirect("/")


@app.route("/produto.html/<id>", methods=['GET'])
def produto(id):
    documentos = collection.find_one({'_id': ObjectId(id)})
    return render_template("produto.html", documentos=documentos)



if __name__ == "__main__":
    app.run(debug=True)
    