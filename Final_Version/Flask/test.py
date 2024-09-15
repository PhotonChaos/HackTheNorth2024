# Initialisation on web server
import cgitb
cgitb.enable()
#print("Content-type: text/html\n\n")
import sys
sys.path.append('/mnt/web305/c1/31/53991431/htdocs/.local/lib/python3.11/site-packages')

from flask import Flask, render_template_string

app = Flask(__name__)

# Sample route that returns HTML

@app.route('/')
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Simple Flask Website</title>
        </head>
        <body>
            <h1>Welcome to the Simple Flask Website!</h1>
            <p>This is a basic example of returning HTML from Flask.</p>
        </body>
        </html>
    """)

# Run the app
if __name__ == "__main__":
    app.run()
