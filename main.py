import flask as web
import basic
import model


location = basic.get_location()

main = web.Blueprint("main", __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if web.request.method == 'GET':
        return web.redirect(location["auth"] + "/login")


@main.route('/<string:username>/home', methods=['GET', 'POST'])
def home(username):
    if web.request.method == 'GET':
        try:
            account = model.User.query.get_or_404(username)
            if account.username == username and account.online == True:
                return web.render_template('home.html', user = account,user_location = location["auth"],admin_location = location["admin"])
        except Exception as e:
            return web.render_template("error.html",error="fail to log in home" ,reason = str(e))
