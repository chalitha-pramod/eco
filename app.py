from flask import Flask, render_template, redirect, request, url_for, session
from functools import wraps
import os
import sys
import re
import pyrebase
import uuid


config = {
  "apiKey": "AIzaSyDLUsIE1azEZp83gZFo8qbIbYzE1BZvAQw",
  "authDomain": "trivity-ba193.firebaseapp.com",
  "databaseURL": "https://trivity-ba193-default-rtdb.firebaseio.com",
  "projectId": "trivity-ba193",
  "storageBucket": "trivity-ba193.appspot.com",
  "messagingSenderId": "789439167659",
  "appId": "1:789439167659:web:aeae5d0cf0fb0da9adcbee",
  "measurementId": "G-NE3JF2YYBH"
}
#init firebase
firebase = pyrebase.initialize_app(config)
#auth instance
auth = firebase.auth()
#real time database instance
db = firebase.database();
#storage
storage = firebase.storage()

app=Flask(__name__)
app.secret_key = os.urandom(24)

def isAuthenticated(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
      #check for the variable that pyrebase creates
      if not auth.current_user != None:
          return redirect(url_for('login'))
      return f(*args, **kwargs)
  return decorated_function

@app.route("/", methods=["POST", "GET"])
@isAuthenticated
def index():
  
  return render_template("index.html")

#signup route
@app.route("/signup", methods=["GET", "POST"])
# @isNotLoggedIn
def signup():
  if request.method == "POST":
    #get the request form data
    
    email = request.form["email"]
    password = request.form["password"]
    username = request.form["username"]
    company = request.form["company"]
    title = request.form["title"]
    country = request.form["country"]
    adress = request.form["adress"]



    try: 
      #create the user
      auth.create_user_with_email_and_password(email, password);
      #login the user right away
      user = auth.sign_in_with_email_and_password(email, password)   
      #session
      user_id = user['idToken']
      user_email = email
      session['usr'] = user_id
      session["email"] = user_email
      
      user_data = {"email": email , "password":password ,"company":company ,"title":title ,"country":country,"adress":adress , "username": username, "creditpoints": 1}
      db.child("users").child(auth.current_user["localId"]).update(user_data)

      return redirect("/") 
    except:
      return render_template("signup.html", message="Email is already taken or password has less than 6 letters" )  

  return render_template("signup.html")
  


#login route
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    #get the request data
    email = request.form["email"]
    password = request.form["password"]
    try:
      #login the user
      user = auth.sign_in_with_email_and_password(email, password)
      #set the session
      user_id = user['idToken']
      user_email = email
      session['usr'] = user_id
      session["email"] = user_email

      return redirect("/")
    except:
      return render_template("login.html", message="Wrong Credentials")
  return render_template("login.html")

#logout route
@app.route("/logout")
def logout():
    #remove the token setting the user to None
    auth.current_user = None

    session.clear()
    return redirect("/");

@app.route("/profile", methods=["POST", "GET"])
@isAuthenticated
def profile():
  user_data = db.child("users").child(auth.current_user["localId"]).get().val()
  creditpoints = db.child("users").child(auth.current_user["localId"]).child("creditpoints").get().val()

  if request.method == "POST":
    #get the request form data
    # email = request.form["email"]
    profile_photo =request.form["profile_photo"]
    email = request.form["email"]
    password = request.form["password"]
    username = request.form["username"]
    company = request.form["company"]
    title = request.form["title"]
    country = request.form["country"]
    adress = request.form["adress"]
   

    # Check if a change was made
    # If no (input field is empty) than overwrite the update info with the previous information
    # Do this for every asked information
    # if email == "":
    #   email = user_data["email"]
    # elif email != "":
    #   auth.setAccountInfo
    if profile_photo == "":
      profile_photo = user_data["profile_photo"]
    if email == "":
      email = user_data["email"]
    if password  == "":
      password  = user_data["password "]
    if username == "":
      username = user_data["username"]      
    if company == "":
      company = user_data["company"]
    if title == "":
      title = user_data["title"]
    if country == "":
      country = user_data["country"] 
    if adress == "":
      adress = user_data["adress"] 
      

    user_data = {"profile_photo": profile_photo, "email": email, "password": password,"username": username,"company": company,"title": title,"country": country,"adress": adress, "creditpoints": 0}
    db.child("users").child(auth.current_user["localId"]).update(user_data)

    # next line could in theory be forgotten
    user_data = db.child("users").child(auth.current_user["localId"]).get().val()
    return render_template("profile.html", user_infos=user_data, session_username=username, creditpoints=creditpoints)
  return render_template("profile.html", user_infos=user_data, session_username=user_data["username"], creditpoints=creditpoints)



#addnew route
@app.route("/addnew", methods=["GET", "POST"])
@isAuthenticated
def addnew():
  user_project = db.child("user_project").child(auth.current_user["localId"]).get().val()
  creditpoints = db.child("user_project").child(auth.current_user["localId"]).child("creditpoints").get().val()
  if request.method == "POST":
    #get the request data
    pname = request.form["pname"]
    sname = request.form["sname"]
    tagline = request.form["tagline"] 
    keyfeatures = request.form["keyfeatures"]
    title = request.form["title"]
    profitability = request.form["profitability"]
    detail = request.form["detail"]
    filename0 = str(uuid.uuid0())+os.path.splitext(image.filename)[0]
    scs = request.form["scs"]
    scb = request.form["scb"]
    selectcountry = request.form["selectcountry"]
    city = request.form["city"]
    city = request.form["town"]
    city = request.form["street"]
    pir = request.form["pir"]
    pt = request.form["pt"]
    acc = request.form["acc"]
    filename1= str(uuid.uuid1())+os.path.splitext(image.filename)[1]
    filename2= str(uuid.uuid2())+os.path.splitext(image.filename)[2]
    filename3= str(uuid.uuid3())+os.path.splitext(image.filename)[3]
    filename4= str(uuid.uuid4())+os.path.splitext(image.filename)[4]
     
    


    user_project = {
      "pname":pname,
      "sname":sname ,
      "tagline":tagline ,
      "keyfeatures":keyfeatures ,
      "title":title ,
      "profitability":profitability ,
      "detail":detail,
      "filename0":filename0,
      "scs":scs ,
      "scb": scb,
      "selectcountry":selectcountry ,
      "city":city ,
      "pir":pir ,
      "pt":pt ,
      "acc":acc ,
      "filename1":filename1 ,
      "filename2":filename2,
      "filename3":filename3 ,
      "filename4":filename4 ,
     

      "author": session["email"]
    }
    try:
      #print(title, content, file=sys.stderr)

      #push the post object to the database
      db.child("user_project").push(user_project)
      user_project = {"pname": pname, "sname": sname, "tagline": tagline,
      "keyfeatures": keyfeatures,"title": title,"profitability": profitability,
      "detail": detail,"filename0": filename0,"scs":scs ,
      "scb": scb,"selectcountry": selectcountry,"city":city ,
      "pir": pir,"pt": pt,"acc":acc ,
      "filename1": filename1,"filename2": filename2,
      "filename3": filename3,"filename4": filename4,
      
      
      
      
       "creditpoints": 0}
      return redirect("/")
    except:
      return render_template("/addnew.html",user_in=user_project,  creditpoints=creditpoints) 
  return render_template("/addnew.html",user_in=user_project) 
      


#projects route
@app.route("/projects")
@isAuthenticated
def projects():

 return render_template("/projects.html") 


@app.route("/index1")
@isAuthenticated
def index1():
 return render_template("/index1.html")
  






if __name__== "__main__":
    app.run(debug=True)
