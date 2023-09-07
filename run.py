from app import create_app
from pyngrok import ngrok
import time
import webbrowser
import threading
import os

app = create_app()
def open_browser():
    time.sleep(5)
    webbrowser.open('http://127.0.0.1:5000', new=3)
if __name__ == "__main__":
    app.config['PUBLIC_URL'] = ngrok.connect(5000).public_url
    print("Public URL:", ngrok.connect(5000).public_url)
    # Only open the web browser when the reloader is not active
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        threading.Thread(target=open_browser).start()
    app.run(debug=True)



