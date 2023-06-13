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


@app.route("/produtos", methods=['GET'])
def produtos():
    documentos = collection.find().limit(80)
    return render_template("produtos.html", documentos=documentos)


@app.route("/add", methods=['GET', 'POST'])
def adicionar():
    if request.method == "GET":
        return render_template("add.html")
    else: 
        new_acessory ={
            "Name" : request.form['nome'],
            "Company" : {
                "Name" : request.form['marca']} ,
            "Category" : request.form['categoria'],
            "Price" : request.form['preco'],
            "Body" : {
                "Location" : request.form['localizacao']} ,
            "Imagem" : request.form['imagem'],
            "Observations" : request.form['obs']
        }

        collection.insert_one(new_acessory)
        logging.info(f"Produto inserido com sucesso: {new_acessory}")
        
        return redirect(url_for("home"))
    

@app.route("/edit/<id>", methods=[ 'GET', 'POST']) 
def edit(id): 
    if request.method=='GET':
        documentos = collection.find_one({"_id" : ObjectId(id)})
        return render_template("edit.html", documentos=documentos)
    
    else :
        updated_document = {
            "Name" : request.form['nome'],
            "Company" : {
                "Name" : request.form['marca']} ,
            "Category" : request.form['categoria'],
            "Price" : request.form['preco'],
            "Body" : {
                "Location" : request.form['loc']} ,
            "Imagem" : request.form['img'],
            "Observations" : request.form['obs']
        }
        collection.update_one({"_id" : ObjectId(id)}, {"$set" : updated_document })
        
        return redirect(url_for("produto_details", id = id))


@app.route("/details/<id>", methods=['GET'])
def produto_details(id):
    documentos = collection.find_one({'_id': ObjectId(id)})
    logging.info(f"Detalhes do produto acessado com sucesso: {ObjectId(id)}")
    return render_template("details.html", documentos=documentos)


@app.route("/deletar/<id>", methods=["POST"])
def delete(id):
    collection.delete_one({'_id': ObjectId(id)})
    logging.info(f"Produto deletado com sucesso: {ObjectId(id)}")
    return redirect(url_for('home'))





if __name__ == "__main__":
    app.run(debug=True)
    
    