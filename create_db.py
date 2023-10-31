from website import db, create_app
from website.models import User
app = create_app()
ctx = app.app_context()
ctx.push()
db.create_all()

# Create a test user after creating tables
new_user = User(
    id= 1,
    name='test', 
    emailid='test@test.com',  
    # Set the hased password
    # password 123
    password_hash='pbkdf2:sha256:600000$nvWS6nmc8Iw7ygGJ$4acbc709f0c12a06bda0a373cf7b6a6abaebf05a6503e671d2a78a55717f6e73'  
)


# Add the test user to the session and commit it to the database
db.session.add(new_user)
db.session.commit()

quit()