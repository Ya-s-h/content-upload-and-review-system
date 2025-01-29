from flask import Blueprint, request, jsonify
from models import Movies

movies_bp = Blueprint("movies", __name__)

@movies_bp.route("/", methods=["GET"])
def get_movies():
    page = int(request.args.get('page', 1))
    per_page = min(20, int(request.args.get('per_page', 20)))
    
    filters= {}
    if "year" in request.args:
        filters["release_date__year"] = int(request.args["year"])  # Filter by year
    if "language" in request.args:
        filters["movie_language"] = request.args["language"]  # Filter by language

    sort_field = request.args.get("sort_by", "release_date")
    sort_order = request.args.get("order", "asc")
    if sort_order not in ("asc", "desc"):
        return jsonify({"error": f"Order value should be asc, desc "}), 400
    
    if sort_field not in ("release_date", "ratings"):
        return jsonify({"error": f"sort_by value should be release_date, ratings "}), 400
    
    sort_direction = "+" if sort_order == "asc" else "-"
    movies = Movies.objects(**filters).order_by(f"{sort_direction}{sort_field}").skip((page-1)*per_page).limit(per_page)
    resp = []
    for movie in movies:
        movie = movie.to_mongo().to_dict()
        movie.pop("_id")
        resp.append(movie)
    return jsonify({
        "movies": resp
    }), 200
