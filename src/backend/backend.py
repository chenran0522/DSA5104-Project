from flask import Flask
from flask_cors import CORS
import image_queries
import book_queries
<<<<<<< HEAD
import game_queries
=======
import music_queries
>>>>>>> 4c13bfd65ac2a9ee6fa4064d352763bee00688e6

app = Flask(__name__)
CORS(app)

app.register_blueprint(image_queries.bp)
app.register_blueprint(book_queries.bp)
<<<<<<< HEAD
app.register_blueprint(game_queries.bp)
=======
app.register_blueprint(music_queries.bp)

>>>>>>> 4c13bfd65ac2a9ee6fa4064d352763bee00688e6
if __name__ == "__main__":
    app.run(debug=True)
