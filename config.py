import os
# config params are just class variables
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'guess_me_sucker'
