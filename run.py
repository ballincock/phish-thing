""" 
Haven't tested importing os or db in production
added env into create_app employment, not tested in production

shell context processor added, not tested in production
before running the app (bottom of file):
   added port, not tested in production
   added host, not tested in production

while running the app in the bottom of the file: specificied the host and port from above
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

    
    app.run(
       host=host, 
       port=port, 
       debug=(env == 'dev'),
       debug=True
    )
