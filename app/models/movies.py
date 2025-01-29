from mongoengine import Document, StringField, IntField, URLField, DateField, FloatField, ListField, DecimalField, connect
connect(db='movies_management', host= "mongodb://localhost:27017/movies_management")


class Movies(Document):
    meta = {
        'indexes': ['movie_title', 'release_date'],  
    }

    budget = DecimalField(default=0, precision=2, min_value=0)
    homepage = URLField()
    movie_language = StringField(required=True)
    movie_og_title = StringField(required=True,unique=True)
    movie_summary = StringField(required=True)
    release_date = DateField()
    revenue = DecimalField(default=0, precision=2, min_value=0)
    runtime_in_minutes = IntField(required=True, min_value=0)
    movie_status = StringField(required=True, choices= ["released", "in_production", "canceled", "rumored", "post_production", "planned"])
    movie_title = StringField(required=True)
    ratings = FloatField(default=0, min_value=0, max_value=10)
    reviews = IntField(default=0, min_value=0)
    production_company_id = IntField(required=True)
    genre_id = IntField(required= True)
    languages = ListField(StringField(), default=["English"])
