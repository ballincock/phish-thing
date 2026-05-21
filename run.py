""" Haven't tested importing os or db in production
"""
import os
from app import create_app, db

app = create_app(env)

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')

    
    app.run(debug=True)
