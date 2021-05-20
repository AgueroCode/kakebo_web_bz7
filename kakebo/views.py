from kakebo import app

@app.route('/')
def index():
    return 'Flask rulando'