from app import app
from app import db
# Get tables from database
from app.models import User, Post

# Add database into shell context
# Command `flask shell` returns this function and registers its returned elems
@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Post':Post}
