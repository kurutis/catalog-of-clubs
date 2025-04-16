from flask import render_template, request, session, redirect, url_for
from hashlib import sha512

from src.views.admin import bp
from src import db
from src.route_filter import require_admin
from src.config import Config


@bp.route("/")
@require_admin
def index():
    print(session.get("message", None))
    return render_template("admin/admin.html", message=session.pop("message", None))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        l, p = request.form.get("login", None), request.form.get("password", None)
        if sha512(f"{l}:{p}".encode()).hexdigest() in Config.ADMIN_AUTH:
            session["logged"] = True
            return redirect("/admin")
    return render_template("admin/login.html")


@bp.route("/logout")
def logout():
    session["logged"] = False
    return redirect("/admin/login")


@bp.route("/edit")
@require_admin
def edit():
    return render_template("admin/edit.html", coteries=db.get_coteries(), message=session.pop("message", None))


@bp.route("/edit/<int:id_>", methods=["GET", "POST"])
@require_admin
def edit_n(id_: int):
    if request.method == "POST":
        db.edit_coterie(id_=id_, new_name=request.form.get("name", None), new_type_id=request.form.get("type", None),
                        new_teacher_id=request.form.get("teacher", None),
                        new_address_id=request.form.get("address", None), new_beg_age=request.form.get("beg-age", None),
                        new_end_age=request.form.get("end-age", None), new_day=request.form.get("day", None),
                        new_price=request.form.get("price", False), new_info=request.form.get("info", None),
                        new_url=request.form.get("url", None))
        session["message"] = "Успешно изменено"
    return render_template("admin/edit_n.html", coterie=db.get_coterie(id_),
                           types=db.get_types(), teachers=db.get_teachers(), addresses=db.get_addresses(),
                           message=session.pop("message", None))


@bp.route("/edit/<int:id_>/delete")
@require_admin
def delete_n(id_: int):
    db.delete_coterie(id_=id_)
    session["message"] = "Успешно удалено"
    return redirect(url_for("admin.edit"))


@bp.route("/add", methods=["GET", "POST"])
@require_admin
def add():
    if request.method == "POST":
        c = db.add_coterie(name=request.form.get("name", None), type_id=request.form.get("type", None),
                           teacher_id=request.form.get("teacher", None), address_id=request.form.get("address", None),
                           beg_age=request.form.get("beg-age", None), end_age=request.form.get("end-age", None),
                           day=request.form.get("day", None), price=request.form.get("price", False),
                           info=request.form.get("info", None), url=request.form.get("url", None))
        if not c[0]:
            print(c)
            return c[1]
        session["message"] = "Успешно добавлено"
        return redirect(url_for("admin.edit_n", id_=c[1]))
    return render_template("admin/add.html", types=db.get_types(), teachers=db.get_teachers(),
                           addresses=db.get_addresses())


@bp.route("/edit-teacher")
@require_admin
def edit_teacher():
    return render_template("admin/edit_teacher.html", teachers=db.get_teachers(), message=session.pop("message", None))


@bp.route("/edit_teacher/<int:id_>", methods=["GET", "POST"])
@require_admin
def edit_teacher_n(id_: int):
    if request.method == "POST":
        c = db.edit_teacher(id_=id_, new_name=request.form.get("name", None),
                            new_photo_url=request.form.get("photo-url", None),
                            new_link=request.form.get("link", None))
        if not c[0]:
            print(c)
            return c[1]
        session["message"] = "Успешно изменено"
    return render_template("admin/edit_teacher_n.html", teacher=db.get_teacher(id_),
                           message=session.pop("message", None))


@bp.route("/edit_teacher/<int:id_>/delete")
@require_admin
def delete_teacher_n(id_: int):
    db.delete_teacher(id_=id_)
    session["message"] = "Успешно удалено"
    return redirect(url_for("admin.edit_teacher"))


@bp.route("/add-teacher", methods=["GET", "POST"])
@require_admin
def add_teacher():
    if request.method == "POST":
        c = db.add_teacher(name=request.form.get("name", None), photo_url=request.form.get("photo-url", None),
                           link=request.form.get("link", None))
        if not c[0]:
            print(c)
            return c[1]
        session["message"] = "Успешно добавлено"
        return redirect(url_for("admin.edit_teacher_n", id_=c[1]))
    return render_template("admin/add_teacher.html")


@bp.route("/edit-address")
@require_admin
def edit_address():
    return render_template("admin/edit_address.html", addresses=db.get_addresses(),
                           message=session.pop("message", None))


@bp.route("/edit_address/<int:id_>", methods=["GET", "POST"])
@require_admin
def edit_address_n(id_: int):
    if request.method == "POST":
        c = db.edit_address(id_=id_, new_address=request.form.get("address", None))
        if not c[0]:
            print(c)
            return c[1]
        session["message"] = "Успешно изменено"
    return render_template("admin/edit_address_n.html", address=db.get_address(id_),
                           message=session.pop("message", None))


@bp.route("/edit_address/<int:id_>/delete")
@require_admin
def delete_address_n(id_: int):
    db.delete_address(id_=id_)
    session["message"] = "Успешно удалено"
    return redirect(url_for("admin.edit_address"))


@bp.route("/add-address", methods=["GET", "POST"])
@require_admin
def add_address():
    if request.method == "POST":
        c = db.add_address(address=request.form.get("address", None))
        if not c[0]:
            print(c)
            return c[1]
        session["message"] = "Успешно добавлено"
        return redirect(url_for("admin.edit_address_n", id_=c[1]))
    return render_template("admin/add_address.html")
