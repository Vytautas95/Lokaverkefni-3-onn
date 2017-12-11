<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet"  href="/static/stylesheet.css">
	<title>Stocks</title>
</head>
<body>
<div class="usercontainer">
	<div class="childcontainer">
		<h3>Notandi: {{name}}</h3>
		<form action="/logout">
			<input value="skrá út" type="submit">
		</form>
	</div>
	<h3  class="childcontainer">
		Peningur: {{cash}}kr<br>
		Heildareign í kr: {{value}}
	</h3>
</div>
<h1>Stock</h1>
<h2>Nafn: {{sname}}</h2>
<h2>Upprunalegt verð: {{ogprice}}</h2>
<h2>Núverandi markaðsverð: {{currprice}}</h2>
<h2>Síðasta prósentu breyting: {{lpercent}}%</h2>
<h2>Eigandi: {{owner}}</h2>
<h2>Verð: {{sprice}}</h2>
<form action="/kaupa" method='POST'>
	<input value="Kaupa" type="submit">
</form>
<p><a href="/stocks/{{lid}}">Skoða seinasta</a> <a href="/stocks/{{nid}}">Skoða næsta</a></p>

</body>
</html>
