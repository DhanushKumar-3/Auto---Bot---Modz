import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "super-secret-key-change-this"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ShopConfig:
    SHOP_NAME = "Auto Bot Modz"
    GST_NUMBER = "29ABCDE1234F1Z5"   # replace with your real GST
    CGST_PERCENT = 9
    SGST_PERCENT = 9
    ADDRESS = "123, Main Street, City, Country"
    PHONE = "+1-234-567-890"
    EMAIL = "autobotmodz@gmail.com"
    FOOTER_NOTE = "Thank you for shopping with Auto Bot Modz!"
    