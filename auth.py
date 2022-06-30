from re import T
import flask as web
import model
import basic
import datetime as dt

location = basic.get_location()

auth = web.Blueprint("auth", __name__)
db = basic.get_db()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if web.request.method == 'GET':
        return web.render_template('login.html', location=location["auth"])
    if web.request.method == 'POST':
        username = web.request.form["username"]
        password = web.request.form["password"]

        try:
            account = model.User.query.get_or_404(username)
        except Exception as e:
            return web.render_template('login.html', location=location["auth"], prompt=f"account is not exist")

        if account.password == password and account.level >= 0: # to check the user which is not in the blacklist
            account.last_online_date = dt.datetime.now()
            account.online = True
            db.session.commit()

            return web.redirect(f"/{username}/home")
        elif account.password == password and account.level < 0:
            return web.render_template('login.html', location=location["auth"], prompt=f"this account have been blocked")
        else:
            return web.render_template('login.html', location=location["auth"], prompt=f"password is not correct", username=username)


@auth.route('/<string:username>/logout', methods=['GET', 'POST'])
def logout(username):
    if web.request.method == 'GET':
        try:
            account = model.User.query.get_or_404(username)
            if account.online == True:
                account.online = False
                db.session.commit()
                return web.render_template('logout.html',user = account)
        except Exception as e:
            return web.render_template('error.html',error ="fail to log out!",reason = str(e))
    return web.redirect("/")
    


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if web.request.method == 'GET':
        return web.render_template('signup.html', location=location["auth"])
    elif web.request.method == 'POST':
        username = web.request.form["username"]
        password = web.request.form["password"]
        try:
            # to check the password
            if web.request.form["password"] == web.request.form["confirm_password"]:
                new_user = model.User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                return web.redirect(location["auth"] + "/login")
            else:  # if not correct just try again
                return web.render_template('signup.html', username=username, password=password, prompt="password is not correct", location=location["auth"])
        except Exception as e:
            return web.render_template('error.html', error="this username is always exist", reason = str(e))
