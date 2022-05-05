from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz
from sqlalchemy import true


app = Flask(__name__)
api = Api(app)

# define location of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    # define all fields in video model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    
# create database, comment out after running first time to
# not reinitialize database
db.create_all() 

resource_fields={
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer,
}

# enables url to have ...video?name=For+You
parser = reqparse.RequestParser()
parser.add_argument("id", type=int, help="ID of video not set.")
parser.add_argument("name", type=str, help="Name of video not set.")
parser.add_argument("views", type=int, help="Views of video not set.")
parser.add_argument("likes", type=int, help="Likes of video not set.")

class Video(Resource):
    # use fuzzy logic to return videos with names similar to the input video name
    @marshal_with(resource_fields)
    def get(self):   
        args=parser.parse_args()
        if args['id']:
            # GET VIDEO VIA ID SEARCH
            video_id = args['id']
            result = VideoModel.query.filter_by(id=video_id).first()
        if args['name']:
            # GET VIDEOS VIA FUZZY LOGIC NAME SEARCH
            video_name = args['name']
            result= VideoModel.query.all()
            results=[]        
            for r in result:   
                fuzz_ratio= fuzz.partial_token_sort_ratio(video_name, r.name)
                if fuzz_ratio >= 70:                
                    results.append(r.name)

            result=VideoModel.query.filter(VideoModel.name.in_(results)).all()
        else:
            result= VideoModel.query.all()
        if not result:
            abort(404, message="No video could be found with that name.")
        return result
        
    # creates video
    @marshal_with(resource_fields)
    def put(self):
        args = parser.parse_args()
        result=VideoModel.query.filter_by(id=args['id']).first()
        if result:
            abort(409, message="Video id taken.")

        video=VideoModel(id=args['id'], name=args['name'], views=args['views'], likes=args['likes'])
        
        # adds obj to cu db session
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self):
        args=parser.parse_args()
        result=VideoModel.query.filter_by(id=args['id']).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot udpate.")

        if args['name']:
            result.name=args['name']
        if args['views']:
            result.views=args['views']
        if args['likes']:
            result.likes=args['likes']

        
        db.session.commit()
        return result

    def delete(self):        
        # returns VideoModel obj with the id
        args=parser.parse_args()
        video_id=args['id']
        result= VideoModel.query.filter_by(id=video_id).first()   
        if not result:
            abort(404, message="Could not find video with that id.")        
        
        # deletes obj from cu db session
        db.session.delete(result)
        db.session.commit()

        # status code 204 means deleted successfully
        return 200

api.add_resource(Video, '/video')

if __name__=='__main__':
    app.run(debug=True)