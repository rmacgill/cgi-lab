#!/usr/bin/env python3

import os
import json
import secret
import requests
import sys
from cgi import escape 

# From templates.py
def login_page():
   return """
   <h1> Welcome! </h1>

   <form method="POST" action="hello.py">
      <label> <span>Username:</span> <input autofocus type="text" name="username"></label> <br>
      <label> <span>Password:</span> <input type="password" name="password"></label>

      <button type="submit"> Login! </button>
   </form>
   """

# From templates.py
def secret_page(username=None, password=None):
   if username is None or password is None:
      raise ValueError("You need to pass both username and password!")

   return """
   <h1> Welcome, {username}! </h1>

   <p>
      <small> Pst! I know your password is
      <span class="spoilers"> {password} </span>
      </small>
   </p>
   """.format(username=escape(username.capitalize()),
              password=escape(password))


# Check for a POST request and set cookies if username and password are correct
postedUsername = None
postedPassword = None

posted_bytes = os.environ.get("CONTENT_LENGTH", 0)
if posted_bytes:
   try:
      posted = sys.stdin.read(int(posted_bytes))
      for line in posted.splitlines():
         for pair in line.split('&'):
            (key, val) = pair.split('=')
            if key == "username" and val == secret.username:
               postedUsername = val
            if key == "password" and val == secret.password:
               postedPassword = val
   except:
      postedUsername = None
      postedPassword = None

if postedUsername != None and postedPassword != None:
   print("Set-Cookie:Username={};".format(postedUsername))
   print("Set-Cookie:Password={};".format(postedPassword))

print("Content-Type: text/html")
print()

print(
"""
<!DOCTYPE html>
<html>
<body>
<ul>
"""
)

# Prints the query parameters
try:
   for param in os.environ["QUERY_STRING"].split('&'):
      (key, val) = param.split('=')
      print("<li><em>{}</em> = {}</li>".format(key, val))
except:
   print("<p>Could not print query parameters.</p>")

print("</ul>")

# Show the browser
print("<p><em>Browser:</em> {}</p>".format(os.environ["HTTP_USER_AGENT"]))

# Show the login form
print(login_page())

#Checks for cookies. If it finds the right ones, shows the secret message
cookieUser = None
cookiePass = None

try:
   for cookie in os.environ["HTTP_COOKIE"].split("; "):
      (key, val) = cookie.split('=')
      if key == "Username":
         cookieUser = val
      if key == "Password":
         cookiePass = val
except:
   print("<p>No cookies.</p>")
   cookieUser = None
   cookiePass = None

if cookieUser != None and cookiePass != None:
   print(secret_page(cookieUser, cookiePass))      

print(
"""
</body>
</html>
"""
)


