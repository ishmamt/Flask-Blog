from flaskblog import db
from flaskblog.models import User, Post

# db.create_all()  # creating the database file. Run once


# adding and creating users
# user_1 = User(username='it', email='it@demo.com', password='1234')
# db.session.add(user_1)
# user_2 = User(username='sv', email='sv@demo.com', password='1234')
# db.session.add(user_2)
# db.session.commit()

# query
# print(User.query.all())  # shows all the users
# print(User.query.first())
# print(User.query.filter_by(username='sv').all())
# print(User.query.get(2))  # searching by id
# print(User.query.get(1))
# print(User.query.get(1).posts)


# lets add a post
# user = User.query.get(1)
# post_1 = Post(title='First Blog', content='Hello World! This is the first ever blog post.', user_id=user.id)
# post_2 = Post(title='The Truth', content='I am the cutest of them all.', user_id=User.query.get(2).id)
# db.session.add(post_1)
# db.session.add(post_2)
# db.session.commit()


# print(User.query.get(1).posts)
# print(User.query.get(2).posts)

# post = Post.query.first()
# print(post)
# print(post.user_id)
# print(post.author)  # refering to the user table

# wiping the slate clean
# db.drop_all()
# db.create_all()
