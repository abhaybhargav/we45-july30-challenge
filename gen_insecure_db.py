from Crypto.Cipher import AES
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import base64
from faker import Faker
import hashlib
import os

PADDING = '{'
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

fake = Faker()

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'


    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    password = Column(String(256), nullable=True)
    ccn = Column(String(256), nullable=True)
    password_hint = Column(String(500), nullable=True)


engine = create_engine('sqlite:///mydb.db')

Base.metadata.create_all(engine)

IV = 'abcdefghijklmnop'

#consider using md5 for protecting CCN

def encrypt_ecb(string):
    enc = AES.new(ekey, AES.MODE_ECB)
    ciphertext = base64.b64encode(enc.encrypt(pad(string)))
    print ciphertext
    return ciphertext

def encrypt_cbc(string, hash):

    enc = AES.new(hash, AES.MODE_CBC, IV)
    ciphertext = base64.b64encode(enc.encrypt(pad(string)))
    print ciphertext
    return ciphertext


DBSession = sessionmaker(bind=engine)
session = DBSession()

def create_user_password(password, hint):

    for i in range(0,10):
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = "{0} {1}".format(first_name, last_name)
        email = fake.email()
        password = password
        password_hint = hint
        ccn = fake.credit_card_number(card_type=None)
        enc_password = encrypt_ecb(password)
        enc_ccn = encrypt_cbc(ccn, hashlib.md5(password).hexdigest())
        new_user = User(name = full_name, password = enc_password, ccn = enc_ccn, password_hint=password_hint)
        session.add(new_user)


session.commit()





