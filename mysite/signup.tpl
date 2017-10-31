<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <meta name="viewport" content="width=device-width">
    <title>SignUp</title>
    <script src="/static/js/signup.js"></script>
    <link href="/static/css/signup.css" rel="stylesheet" type="text/css" />
  </head>

  <body>
<div class="container" >
    <div class="main">
<h2>SignUp</h2>
    <form action="/signup" method="POST">
<label>Email :</label>
    <input name="email" id="email" type="email" placeholder="Email Address"><br>
<label>Password :</label>
    <input name="password" id="password1" type="password" placeholder="Password"><br>
<label>Confirm Password :</label>
    <input name="password" id="password2" type="password" placeholder="Confirm YourPassword">
    <input id="submit" type="submit" value="Signup">
    </form>
    </div>
     <p><a href="http://berlinab.pythonanywhere.com/signin">Click here if you are a returning user</a></p>
<p><b>Note:</b> By default we have Disabled Submit Button,<br>
Please fill complete form with approprite values to enable it.</p>
</div>
</body>
</html>