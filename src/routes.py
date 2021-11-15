import datetime

import requests
from flask_restful import Resource

from src import api, db
from src.models import User


class UsersView(Resource):

    def get(self, id=None):
        """
        file: swagger/users_get.yaml
        """
        if id:
            response = [User.query.get_or_404(id)]
        else:
            response = User.query.all()
        response = [
            {
                'id': item.id,
                'gender': item.gender,
                'first_name': item.first_name,
                'last_name': item.last_name,
                'e_mail': item.e_mail,
                'born_date': datetime.datetime.isoformat(
                    item.born_date
                    ).split('T')[0]
                }
            for item in response
            ]

        return response, 200

    def post(self, id=None):
        """
        file: swagger/users_post.yaml
        """
        count = len(User.query.all())
        added_users = 0
        while count < 100:
            random_user = requests.get('https://randomuser.me/api/').json()
            if random_user['results'][0]['gender'] == 'male':
                user = User(
                    gender=random_user['results'][0]['gender'],
                    first_name=random_user['results'][0]['name'][
                        'first'].encode('utf-8'),
                    last_name=random_user['results'][0]['name']['last'].encode('utf-8'),
                    e_mail=random_user['results'][0]['email'],
                    born_date=datetime.datetime.fromisoformat(
                        random_user['results'][0]['dob']['date'].split('.')[0]
                        )
                    )
                db.session.add(user)
                count += 1
                added_users += 1
        db.session.commit()

        return {
                   'message': {
                       'added_users': added_users, 'users_in_db': count
                       }
                   }, 200

    def delete(self, id):
        """
        file: swagger/users_delete.yaml
        """
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': f'user with id={user.id} successfully deleted'}


api.add_resource(UsersView, "/", "/<int:id>/", strict_slashes=False)
