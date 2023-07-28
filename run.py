from app import create_app
from pyngrok import ngrok

app = create_app()

if __name__ == "__main__":
    public_url = ngrok.connect(5000)
    print("Public URL:", public_url)
    app.run(debug=True)
