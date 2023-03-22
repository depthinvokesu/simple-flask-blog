from datetime import datetime
import re
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from application import db, login_manager




def slugify(title) -> str:
    p = r'[^\w]'
    slug = re.sub(p, '-', title)
    slug = slug.lower().strip('-')
    return slug


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship("Tag", back_populates="posts", secondary="atable")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.title = kwargs.get("title")
        self.body = kwargs.get("body")
        self.created = kwargs.get("created")
        self.slug = slugify(self.title)
    
    def __repr__(self) -> str:
        return "<Post: {}>".format(self.slug)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    posts = db.relationship("Post", back_populates="tags", secondary="atable")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.name = kwargs.get('name')
        self.slug = slugify(self.name)

    def __repr__(self) -> str:
        return "<Tag: {}>".format(self.slug)


atable = db.Table(
    "atable",
    db.Column("post_id", db.ForeignKey("post.id", name="fk_atable_post_id")),
    db.Column("tag.id", db.ForeignKey("tag.id", name="fk_atable_tag_id"))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    token = db.Column(db.String(200), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", back_populates="users")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_role(self, role='User'):
        """Set a role (User | Admin) to a user. Default argument is User role"""
        role_obj = db.session.scalars(db.select(Role).where(Role.name == role)).first()
        self.role = role_obj

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Role(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    users = db.relationship("User", back_populates="role")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name")

    def __repr__(self):
        return '<Role {}>'.format(self.name)



# Usage of migrations in CMD. If Migration object is created in a file app.py, below is enough. 
# If file name is different, the usage would be: "flask --app app_name.py db cmd_name"
# PS Here "db" is a command of flask (not a name of SQLAlchemy object) and it's always the same

# Runs at first time to create necessary files and folders
# flask db init

# Runs after model (schema) change
# flask db migrate -m "Initial migration"

# Runs after previous command to persist changes
# flask db upgrade 




# p = Post(
#     title = "Very unique post",
#     body = "It does not have tags"
# )

# with app.app_context():
    # post = db.session.scalars(db.select(Post).where(Post.slug.contains("first"))).first()
    # print(post)
    # t1 = db.session.get(Tag, 1)
    # t2 = db.session.get(Tag, 2)
    # print(t1,t2)
    # p.tags.extend([t1, t2])
    # print(p)
    # db.session.add_all([p])
    # db.session.commit()
    # pass

