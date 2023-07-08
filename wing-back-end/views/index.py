from controller.WebEvent import WebEvent

def html(state):
    # html code ...
    html = """
    <html>
    <head>
    <title>Pico W Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
    html{font-family: Helvetica; display:inline-block; margin: 0px auto; textalign: center;}
    h1{color: #0F3376; padding: 2vh;}
    p{font-size: 1.5rem;}
    button{display: inline-block; background-color: #4286f4; border: none;borderradius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin:
    2px; cursor: pointer;}
    button2{background-color: #4286f4;}
    </style>
    </head>
    <body> <h1>Pico W Web Server</h1>
    <p>GPIO state: <strong>""" + state + """</strong></p>
    <p><a href="/?state=rainbow"><button class="button">rainbow</button></a></p>
    <p><a href="/?state=fill"><button class="button button2">fill</button></a></p>
    <p><a href="/?state=chase"><button class="button button2">chase</button></a></p>
    </body>
    </html>
    """
    return html

def index(event: WebEvent):
    event.responseData = html('NONE')
