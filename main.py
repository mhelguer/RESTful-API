from flask import Flask, request, session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


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

    # repr method to print something valid out
    # def __repr__(self):
    #     return f"Video(name = {name}, views = {views}, likes = {likes})"

# create database, comment out after running first time to
# not reinitialize database
#db.create_all() 

# parse thru req being sent and make sure it fits guidelines
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of video not set.", required=True)
video_put_args.add_argument("views", type=int, help="Views of video not set.")
video_put_args.add_argument("likes", type=int, help="Likes of video not set.")

video_update_args=reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of video not set.")
video_update_args.add_argument("views", type=int, help="Views of video not set.")
video_update_args.add_argument("likes", type=int, help="Likes of video not set.")

resource_fields={
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer,
}

class Video(Resource):
    # use fuzzy logic to return videos with names similar to the input video name
    @marshal_with(resource_fields)
    def get(self):        
        # GET ALL VIDEOS
        result= VideoModel.query.all()
        return
        # GET VIDEO VIA ID SEARCH
        #result = VideoModel.query.filter_by(id=video_id).first()
        return result
        
        # GET VIDEO VIA NAME SEARCH
        '''
        results=[]        
        for r in result:   
            fuzz_ratio= fuzz.partial_token_sort_ratio(video_name, r.name)
            if fuzz_ratio >= 70:                
                results.append(r.name)

        result=VideoModel.query.filter(VideoModel.name.in_(results)).all()
        '''

        if not result:
            abort(404, message="Could not find video with that id.")
        
        return result


    # creates video
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result=VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken.")

        video=VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        
        # adds obj to cu db session
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args=video_update_args.parse_args()
        result=VideoModel.query.filter_by(id=video_id).first()
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

    def delete(self, video_id):        
        # returns VideoModel obj with the id
        result= VideoModel.query.filter_by(id=video_id).first()   
        if not result:
            abort(404, message="Could not find video with that id.")        
        
        # deletes obj from cu db session
        db.session.delete(result)
        db.session.commit()

        # status code 204 means deleted successfully
        return '', 204

# Register HelloWorld as resource

# "/" means default url
# add_resouce(<class name>, <route>)
#   - route can have params via putting /helloworld/<string: key_name>
#   - key_name is the key from the key-val pair of the dictionary being returned

# to add video via name:
#api.add_resource(Video, "/video/<string:video_name>") 

# to add video via id:
api.add_resource(Video, "/video/<int:video_id>") 

# seeing if i can add all resources at same time
#api.add_resource(Video, "/video/<int:video_id>", '/fo', "/video/<string:video_name>")


if __name__=='__main__':
    app.run(debug=True)