from flask import Flask
from flask_cors import CORS
import image_queries
import book_queries
import game_queries

app = Flask(__name__)
CORS(app)

app.register_blueprint(image_queries.bp)
app.register_blueprint(book_queries.bp)
app.register_blueprint(game_queries.bp)
if __name__ == "__main__":
    app.run(debug=True)
