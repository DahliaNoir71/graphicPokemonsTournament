from flask import Flask
from services.routes_service import register_routes

app = Flask(__name__)

# Register the routes defined in the routes module
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
