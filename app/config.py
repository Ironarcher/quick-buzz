#email server support
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = '465'
MAIL_USE_TILS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

#administrator list
ADMINS = ['arpad.kovesdy@gmail.com']