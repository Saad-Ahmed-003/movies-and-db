# app/routes.py
from flask import Blueprint, jsonify
from .db import get_db_connection
import mysql.connector

api_bp = Blueprint('api', __name__)

@api_bp.route('/movies', methods=['GET'])
def get_movies():
    """Returns a list of movies from the database."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT title, description, director, release_date, actors FROM movies;")
        movies_data = []
        for (title, description, director, release_date, actors) in cursor:
            movie = {
                "title": title,
                "description": description,
                "director": director,
                "release_date": release_date.strftime('%Y-%m-%d'),
                "actors": actors.split(', ')
            }
            movies_data.append(movie)
        connection.close()
        return jsonify(movies_data)
    except mysql.connector.Error as err:
        print(f"Error fetching data from database: {err}")
        return jsonify({"error": "Failed to retrieve data from the database."}), 500
