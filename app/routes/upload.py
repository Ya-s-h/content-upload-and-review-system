import io
import json
from flask import Blueprint, request, jsonify
from pandas import read_csv, isna
from datetime import datetime
from models import Movies
from mongoengine import ValidationError

upload_bp = Blueprint("upload", __name__)

import re
def clean_url(url):
    # Combined regex to check for multiple 'http://' or 'https://', spaces, and malformed URLs
    pattern = r'(https?://){2,}|[^\S\r\n]+'
    
    # Check for invalid cases in one step
    if re.search(pattern, url):
        return None

    # Regex for a valid URL, only allowing ASCII characters in domain names
    regex = r'https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
    match = re.match(regex, url)
    return url if match and match.group(0) == url else None
    # Check if the URL matches the valid URL pattern
    return url if re.match(regex, url) else None



@upload_bp.route("/", methods=["POST"])
def upload_csv():
    """Upload and process a CSV file to add movie data."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file format. Only CSV allowed."}), 400
    
    # Read CSV only once
    file_stream = io.BytesIO(file.read())
    df = read_csv(file_stream)
    df.dropna(inplace=True)
    df.drop_duplicates(subset=['title'])
    # Prepare movies to insert
    movies_to_insert = []
    
    for index, row in df.iterrows():
        try:
            # Handle the language string conversion once
            homepage = clean_url(row['homepage'])
            if homepage is None:
                continue
            language_string = row['languages']
            language_string = re.sub(r'\\\\x([0-9A-Fa-f]{2})', r'\\x\1', language_string)  # Handle encoding issues
            language_string = language_string.replace("'", '"').replace("\\", "\\\\")
            
            try:
                release_date = datetime.strptime(row["release_date"], "%d-%m-%Y")
            except ValueError:
                release_date = datetime.strptime(row["release_date"], "%Y-%m-%d")
            
            # Build the movie object
            movie = Movies(
                budget=float(row["budget"]) if isinstance(row["budget"], (int, float)) else 0,
                homepage=homepage,
                movie_language=row['original_language'],
                movie_og_title=row['original_title'],
                movie_summary=row['overview'],
                release_date=release_date,
                revenue=float(row["revenue"]) if isinstance(row["revenue"], (int, float)) else 0,
                runtime_in_minutes=row['runtime'],
                movie_status=row['status'].lower().replace(" ", "_") if not isna(row['status']) else "rumored",
                movie_title=row['title'].lower(),
                vote_average=float(row["vote_average"]) if isinstance(row["vote_average"], (int, float)) else 0,
                vote_count=float(row["vote_count"]) if isinstance(row["vote_count"], (int, float)) else 0,
                production_company_id=row['production_company_id'],
                genre_id=row['genre_id'],
                languages=json.loads(language_string)
            )
            # Append to the list to be inserted
            # movie.validate()
            movies_to_insert.append(movie)
        except Exception as e:
            return jsonify({"error": f"Error processing row number {index + 1}: {row.to_dict()}, {str(e)}"}), 400

    # Validate and insert movies
    if movies_to_insert:
        for movie in movies_to_insert:
            movie.validate()  # Validate each movie
        Movies.objects.delete()
        Movies.objects.insert(movies_to_insert)  # Bulk insert into MongoDB

    return jsonify({"message": "CSV uploaded successfully", "movies_added": len(movies_to_insert)}), 201
