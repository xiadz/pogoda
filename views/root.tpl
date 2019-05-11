<!doctype html>
<html lang="en" class="no-js">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather station</title>
    <link rel="stylesheet" href="/static/style.css">
</head>

<body>
  <header>
    <div id="logo"><img src="/static/logo.png">Weather&nbsp;Station</div>
    <nav>
      <ul>
        <li><a href="/">Home</a>
      </ul>
    </nav>
  </header>

  <section>
    <strong>Current readings</strong>
  </section>

  <section id="pageContent">
    <article>
      <p>Temperature: {{ temperature }} °C</p>
      <p>&nbsp;</p>
      <p>Humidity: {{ humidity }} %</p>
    </article>
   </section>

   <footer>
      2019, Katarzyna Osowska, Marcin Osowski
   </footer>

</body>
</html>
