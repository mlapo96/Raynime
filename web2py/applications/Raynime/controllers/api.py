# api methods

@auth.requires_login()
def hello():
    return dict(message='hello %(email)s' % auth.user)