<!DOCTYPE html>
<html>
<head>
	<title>Admin</title>
</head>
<body>
<form action="/bots" method='POST'>
	<h3>Fjöldi bots</h3>
	<input type="number" name="botfj">
	<h3>upper risk</h3>
	<input type="number" name="upperrisk">
	<h3>lower risk</h3>
	<input type="number" name="lowerrisk">
	<h3>buy risk</h3>
	<input type="number" name="buyrisk">
	<input type="submit" value="skapa">
</form>
<form action="/stocks" method='POST'>
	<h3>Fjöldi Hlutabréfa</h3>
	<input type="number" name="stockfj">
	<h3>Heiti</h3>
	<input type="text" name="name"> 
	<h3>Markaðsverð</h3>
	<input type="number" name="mprice">
	<h3>Upphafleg prósentubreyting</h3>
	<input type="number" name="npchange">
	<input type="submit" value="skapa">
</form>
<form action="/">
	<input type="submit" value="skrá út">
</form>
</body>
</html>
