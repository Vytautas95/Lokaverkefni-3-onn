<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet"  href="/static/stylesheet.css">
	<title>Mín Stocks</title>
</head>
<body>
<div class="usercontainer">
	<div class="childcontainer">
		<h3>Notandi: {{name}}</h3>
		<form action="/logout">
			<input value="skrá út" type="submit">
		</form>
		<form action="/stocks/1">
			<input value="skoða öll hlutabréf" type="submit">
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
<form action="/selja" method='POST'>
	<input type="number" name="price">
	<input value="Setja á sölu" type="submit">
</form>
<p><a href="/minbref/{{lid}}">Skoða seinasta</a> <a href="/minbref/{{nid}}">Skoða næsta</a></p>

</body>
</html>