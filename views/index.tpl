<!DOCTYPE html>
<html>
<head>
	<title>verkefni 10</title>
</head>
<body>
<form  action="/newuser" method="post" accept-charset="ISO-8859-1">
	<h1>Nýr notandi?</h1><br>
	<input type="text" name="newuser"><br>
	<input type="text" name="newpass"><br>
	<input type="submit" value="skrá nýjan user"><br>
</form>
<form  action="/login" method="post" accept-charset="ISO-8859-1">
	<h1>Login</h1><br>
	<input type="text" name="username"><br>
	<input type="password" name="password"><br>
	<input type="submit" value="login">
</form>
</body>
</html>