<!DOCTYPE html>
<html>
<head>
	<title>Stocks</title>
</head>
<body>
<h1>Forsíða</h1>
<h2>Notandi</h2>
<h3>{{name}}</h3>
Peningur: {{cash}}kr
Heildareign í kr: {{value}}
<h1>Stocks</h1>
Nafn: {{sname}}
Upprunalegt verð: {{ogprice}}
Núverandi markaðsverð: {{currprice}}
Síðasta prósentu breyting: {{lpercent}}%
Eigandi: {{owner}}
Verð: {{sprice}}
<a href="/stocks/{{nid}}">Skoða næsta</a>
<form action="/logout">
	<input name="Skrá út" type="submit" name="logout">
</form>
</body>
</html>