from auth import auth
from main import main
from admin import admin
import basic


app = basic.get_app()
db = basic.get_db()
location = basic.get_location()


app.register_blueprint(auth, url_prefix=location["auth"])
app.register_blueprint(main, url_prefix=location["main"])
app.register_blueprint(admin, url_prefix=location["admin"])


def run():
    app.run("0.0.0.0", port=12345, debug=True)


if __name__ == "__main__":
    run()
