"""Views for registration user and confirm registration user in system"""
from datetime import datetime

from cornice import Service
from passlib.hash import pbkdf2_sha256
from passlib.totp import generate_secret
from pyramid.view import view_config
from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from server.models.user import User
from server.models.user_status import UserStatus
from server.models.role import Role


register = Service(name='registration', path='/registration')
confirm_register = Service(name='email_confirm', path='/email_confirm/{email_confirm}')


@register.post()
def registration_view(request):
    """Registration view

    This function get email and password from json request, check if email
    isn't in db - add email and password into db, set status_id to 'Non_active',
    generate and send url-token to user email.
    """
    json = request.json_body
    user_query = User.get_one(request, email=request.json_body['email'])
    if user_query is None:
        url_token_confirmation = generate_secret()
        User.add_user(request, email=request.json['email'],
                      password=pbkdf2_sha256.hash(request.json['password']),
                      url_token=url_token_confirmation,
                      status_id=UserStatus.get_user_by_status(request, status="Non_active").id,
                      create_date=datetime.now())
        mailer = request.mailer
        message = Message(subject="confirm email",
                          sender="asstelite@gmail.com",
                          recipients=[json['email']],
                          body=request.route_url('email_confirm', email_confirm=url_token_confirmation))
        mailer.send_immediately(message, fail_silently=False)

        return {"msg": "We sent token to your email address"}
    else:
        return {"msg": "Your email address is already registered"}


@confirm_register.get()
def confirm_registration_view(request):
    """Confirm registration view

    This function get url_token, check if it isn't in db
    return the 404 Error. If url_token is in db, this function
    create url address, change status_id to 'Active', and set role_id to 'user'.
    """
    user_email_token = request.matchdict['email_confirm']
    non_active_user = User.get_one(request, url_token=user_email_token)
    if non_active_user is None:
        return HTTPNotFound()
    else:
        non_active_user.status_id = UserStatus.get_user_by_status(request, status="Active").id
        non_active_user.role_id = Role.get_role(request, role="user").id
        non_active_user.url_token = None
        return {"msg": "Your email address is confirmed"}