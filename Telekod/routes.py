from Telekod import app
from Telekod.main.routes import main
from Telekod.auth.routes import auth


app.register_blueprint(main)
app.register_blueprint(auth)
