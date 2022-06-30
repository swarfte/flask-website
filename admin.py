import flask as web
import model
import basic
import hashlib

location = basic.get_location()

admin = web.Blueprint("admin", __name__)
db = basic.get_db()


@admin.route('/member', methods=['GET', 'POST'])
def member():
    if web.request.method == 'GET':
        return web.render_template('admin.html',location=location["admin"])
    elif web.request.method == 'POST':
        username = web.request.form["username"]
        password = web.request.form["password"]
        try:
            account = model.User.query.get_or_404(username)
            if account.password == password and account.level == 1: # is super user
                users = model.User.query.order_by(model.User.last_online_date).all()
                return web.render_template('member.html',location=location["admin"],users = users)
            elif account.password == password and account.level != 1: # if not super user
                account.level = -1
                account.online = False
                db.session.commit()
                return web.redirect(location["main"])
        except Exception as e:
            return web.render_template("error.html", error="Access fail" , reason = str(e))

@admin.route('/delete/<string:username>/<string:password>', methods=['GET', 'POST'])
def delete(username, password):
    if web.request.method == 'GET':
        user = model.User.query.get_or_404(username)
        try:
            db.session.delete(user)
            db.session.commit()
            return web.redirect(location["admin"] + '/member')
        except Exception as e:
            return web.render_template("error.html", error="Delete fail!")


@admin.route('/update/<string:username>/<string:password>', methods=['GET', 'POST'])
def update(username, password):
    if web.request.method == 'GET':
        try:
            user = model.User.query.get_or_404(username)
            return web.render_template("update.html", user = user, location=location["admin"], prompt="modify the date that update")
        except Exception as e:
            return web.render_template("error.html", error="Update fail",reason= str(e))
    elif web.request.method == 'POST':
        try:
            user = model.User.query.get_or_404(username)
            user.username = web.request.form["username"]
            user.password = web.request.form["password"]
            user.level = web.request.form["level"]
            db.session.commit()
            return web.redirect(location["admin"] + "/member")
        except Exception as e:
            return web.render_template("error.html", error="Update fail")
