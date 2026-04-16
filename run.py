import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/api')

from api.app import create_app

app = create_app()

with app.app_context():
    from api.models import db
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

