from mongoengine import Document, StringField, IntField, URLField, DateField, FloatField, ListField, DecimalField

class Movies(Document):
    meta = {
        'collection': 'movies',
        'indexes': ['movie_title', 'release_date'],  
    }

    budget = DecimalField(default=0, precision=2, min_value=0)
    homepage = URLField(default=None, null=True)
    movie_language = StringField(required=True)
    movie_og_title = StringField(required=True)
    movie_summary = StringField(required=True)
    release_date = DateField(required=True)
    revenue = DecimalField(default=0, precision=2, min_value=0)
    runtime_in_minutes = IntField(required=True, min_value=1)
    movie_status = StringField(required=True, choices= ["released", "in_production", "cancelled"])
    movie_title = StringField(required=True, unique=True)
    vote_average = FloatField(default=0, min_value=0, max_value=10)
    vote_count = IntField(default=0, min_value=0)
    production_company_id = IntField(required=True)
    genre_id = IntField(required= True)
    languages = ListField(StringField(), default=["English"])
