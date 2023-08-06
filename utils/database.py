from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import inspect

app = Flask(__name__)
db_sqlalchemy = SQLAlchemy()
date_format = '%d/%m/%Y %H:%M'

class User(db_sqlalchemy.Model):
    __tablename__ = 'user'

    id = db_sqlalchemy.Column(db_sqlalchemy.Integer, primary_key=True)
    username = db_sqlalchemy.Column(db_sqlalchemy.String(64), unique=True)
    url = db_sqlalchemy.Column(db_sqlalchemy.String(64), unique=True)   
    db = db_sqlalchemy.Column(db_sqlalchemy.String(64), unique=True)
    password = db_sqlalchemy.Column(db_sqlalchemy.String(64) )
    nick_name = db_sqlalchemy.Column(db_sqlalchemy.String(64))
    phone_number  = db_sqlalchemy.Column(db_sqlalchemy.String(20), nullable=False)
    messages = db_sqlalchemy.relationship('Message', backref='user', lazy=True)
    entity_memory = db_sqlalchemy.Column(db_sqlalchemy.PickleType, nullable=True)
    token = db_sqlalchemy.Column(db_sqlalchemy.String(64))
    created_at = db_sqlalchemy.Column(db_sqlalchemy.DateTime, default=datetime.utcnow, nullable=False, unique=True)

    def __repr__(self):
        # return f'<User {self.id}: phone_number={self.phone_number}, entity_memory={self.entity_memory}>'
        # return f'<user_id {self.id}: username={self.username}, url={self.url}, db={self.db}, nick_name={self.nick_name}, phone_number={self.phone_number}, entity_memory={self.entity_memory} ,  created_at={self.created_at.strftime(date_format)}>'
        return f'<user_id {self.id}: username={self.username}, url={self.url}, db={self.db}, nick_name={self.nick_name}, phone_number={self.phone_number}, created_at={self.created_at.strftime(date_format)}>'
    
    
class Message(db_sqlalchemy.Model):
    __tablename__ = 'message'
    id = db_sqlalchemy.Column(db_sqlalchemy.Integer, primary_key=True)
    user_id = db_sqlalchemy.Column(db_sqlalchemy.Integer, db_sqlalchemy.ForeignKey('user.id'), nullable=False)
    user_name = db_sqlalchemy.Column(db_sqlalchemy.String(80), nullable=True)
    sender = db_sqlalchemy.Column(db_sqlalchemy.String(80), nullable=False)  
    recipient = db_sqlalchemy.Column(db_sqlalchemy.String(80), nullable=False) #sama dengan mobile_phone
    past = db_sqlalchemy.Column(db_sqlalchemy.Text, nullable=False)
    generated = db_sqlalchemy.Column(db_sqlalchemy.Text, nullable=False)
    timestamp = db_sqlalchemy.Column(db_sqlalchemy.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<message_id {self.id}: timestamp={self.timestamp.strftime(date_format)}, recipient={self.recipient}, past={self.past}, sender={self.sender}, generated={self.generated}>'



def inspect_db():
    # Create a context for the current app
    with app.app_context():
        # Get engine
        engine = db_sqlalchemy.engine
           
        
        # Initiate inspection
        inspector = inspect(engine)

        # Ketika mau drop di un-comment dulu
        # db_sqlalchemy.drop_all()
        # user.__table__.drop(db_sqlalchemy.engine)


        # Get table names
        tables = inspector.get_table_names()


        print("Tables:", tables)
        print(f'Total tables: {len(tables)}. [database.py]')

        # Get columns for each table
        for table in tables:
            print("Table Name: ", table)
            
        return tables



def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///user_data.db'
    db_sqlalchemy.init_app(app)
    
    with app.app_context():
        db_sqlalchemy.create_all()


#   return f'<message_id {self.id}: timestamp={self.timestamp.strftime(date_format)}, recipient={self.recipient}, past={self.past}, sender={self.sender}, generated={self.generated}>'


#Fungsi untuk tulis record chat ke database
def write_chat_to_db(user_name, recipient, past, sender ,generated):

    msg = Message(
                user_id=1,
                user_name=user_name,
                recipient=recipient,
                past=past,
                sender=sender,
                generated=generated,
                timestamp=datetime.now())

    with app.app_context():
        db_sqlalchemy.session.add(msg)  # Menambahkan objek pesan masuk ke database
        db_sqlalchemy.session.commit()  # Menyimpan perubahan ke database

    print(f"Message from {recipient} added to database")
    return msg


init_app(app)
inspect_db()



