from crypt import methods
from distutils.log import error
from email import message
from app import app, db, Autor
from app.model import autor
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from datetime import datetime

@app.route("/autor/add", methods=["POST"])
def autor_add():
    data = request.get_json()

    autor= Autor(
        nome = data["nome"],
        nascimento = datetime.strptime(data["nascimento"], "%Y-%m-%d")
    )
    db.session.add(autor)
    try:
        db.session.commit()
    except(IntegrityError):
        return jsonify({"error": True, "message": "Ocorreu um erro ao salvar os dados"})

    return jsonify({"error": False, "message": "Autor criado com sucesso!"})


@app.route("/autor/edit/<id>", methods=["PUT"])
def autor_edit(id):
    data = request.get_json()
    autor = Autor.query.get(id)

    if autor is None:
        return jsonify({
            "message": "Não encontrado",
            "error": True
        }), 404

    autor.nome = data["nome"]
    try:
        db.session.commit()
    except(IntegrityError):
        return jsonify({"error": True, "message": "Ocorreu um erro ao EDITAR"})

    return jsonify ({"error": False, "message": "Editado com sucesso"})

@app.route("/autor/delete/<id>", methods=["DELETE"])
def autor_delete(id):

    autor = Autor.query.get(id)

    if autor is None:
        return jsonify({
            "message": "Não encontrado",
            "error": True
        }), 404

    db.session.delete(autor)
    try:
        db.session.commit()
    except(IntegrityError):
        return jsonify({"error": True, "message": "Ocorreu um erro ao DELETAR"})

    return jsonify ({"error": False, "message": "DELETADO com sucesso"})

@app.route("/autor/view/<id>", methods=["GET"])
def autor_view(id):
    autor = Autor.query.get(id)

    if autor is None:
        return jsonify({
            "message": "Não encontrado",
            "error": True
        }), 404

    return jsonify({
        "data": autor.to_dict(),
        "error": False
    })

@app.route("/autor/list", methods=["GET"])
def autor_list():
    autores = Autor.query.all()
    output = {"data": [], "error": False}
    for autor in autores:
        output["data"].append(autor.to_dict())
    return jsonify(output)