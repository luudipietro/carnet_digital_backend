from flask import Flask

app = Flask(__name__)

@app.route('/')
def devolver_listado_socios():
    return 'Listado de socios aun no vinculado'


if __name__ == '__main__':
    app.run(debug=True)