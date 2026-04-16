from api.app import create_app
from api.models import db, User, Note

app = create_app()

with app.app_context():
    # Clear existing data
    db.session.query(Note).delete()
    db.session.query(User).delete()
    db.session.commit()
    
    # Create 3 users with known pw
    users = []
    usernames = ['user1', 'user2', 'user3']
    password = 'password123'
    for username in usernames:
        if not User.query.filter_by(username=username).first():
            user = User(username, password)
            db.session.add(user)
            users.append(user)
    
    db.session.commit()
    
    # Create 3 notes per user
    titles = ['Morning journal', 'Daily task list', 'Evening reflection']
    contents = ['Today I woke up early.', 'Todo: buy milk, call mom.', 'Great day overall.']
    for user in users:
        for i in range(3):
            note = Note(title=titles[i], content=contents[i], user_id=user.id)
            db.session.add(note)
    
    db.session.commit()
    
    print('Seeded 3 users (user1-3 pw: password123) with 9 notes')

