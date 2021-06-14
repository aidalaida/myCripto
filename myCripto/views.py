from myCripto import app

@app.route('/')
def index():
    return 'Flask rula'