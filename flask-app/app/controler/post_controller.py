from crypt import methods
from distutils.log import error
from email import message
from app import app, db, Post
from app.model import post
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

@app.route("/post/add", methods=["POST"])
def post_add():
    data = request.get_json()

    post= Post(
        titulo = data["titulo"],
        conteudo = data["conteudo"],
        autor_id = data["autor_id"]

    )
    db.session.add(post)
    try:
        db.session.commit()
    except(IntegrityError):
        return jsonify({"error": True, "message": "Ocorreu um erro ao salvar os dados"})

    return jsonify({"error": False, "message": "Post criado com sucesso!"})

@app.route("/post/edit/<id>", methods=["PUT"])
def post_edit(id):
    data = request.get_json()
    post = Post.query.get(id)

    if post is None:
        return jsonify({
            "message": "Não encontrado",
            "error": True
        }), 404

    post.titulo = data["titulo"]
    post.conteudo = data["conteudo"]
    post.autor_id = data["autor_id"]

    try:
        db.session.commit()
    except(IntegrityError):
        return jsonify({"error": True, "message": "Ocorreu um erro ao EDITAR"})

    return jsonify ({"error": False, "message": "Editado com sucesso"})

@app.route("/post/delete/<id>", methods=["DELETE"])
def post_delete(id):

    post = Post.query.get(id)

    if post is None:
        return jsonify({
            "message": "Não encontrado",
            "error": True
        }), 404

    db.session.delete(post)
    try:
        db.session.commit()
    except(IntegrityError):
        return jsonify({"error": True, "message": "Ocorreu um erro ao DELETAR"})

    return jsonify ({"error": False, "message": "DELETADO com sucesso"})

@app.route("/post/view/<id>", methods=["GET"])
def post_view(id):
    post = Post.query.get(id)

    if post is None:
        return jsonify({
            "message": "Não encontrado",
            "error": True
        }), 404

    return jsonify({
        "data": post.to_dict(),
        "error": False
    })

@app.route("/post/list", methods=["GET"])
def post_list():
    posts = Post.query.all()
    output = {"data": [], "error": False}
    for post in posts:
        output["data"].append(post.to_dict())
    return jsonify(output)