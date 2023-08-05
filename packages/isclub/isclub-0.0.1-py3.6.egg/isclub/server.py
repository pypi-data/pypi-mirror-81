# Flask Object
from flask import Flask

# Extension Object
from .extensions import db
# Settings Object
from .settings import DevConfig

app = Flask("isclub")
app.config.from_object(DevConfig)

# Register App
if __name__ == "__main__":
    # BluePrints Object
    from index import index_bp
    from webpack import webpack_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(webpack_bp)
    app.run()
