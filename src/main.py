from flask import Flask, render_template, redirect, request, url_for
from libreria import *
import os

# docker-compose up para arrancar el proyecto desde el contenedor
# SI HAY ALGUN CAMBIO GORDO EN MAIN TIENES QUE HACER OTRO BUILD:
    # ( SI NOS PASA QUE DEJA DE FUNCIONAR )


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        necesario = float(request.form.get('necesario'))
        form_iva = float(request.form.get('iva'))
        form_irpf = float(request.form.get('irpf'))

        cal01 = ((form_iva - form_irpf) /100) +1
        subtotal = round(necesario / cal01, 2)

        irpf = round((subtotal * (form_irpf / 100)), 2)
        iva = round((subtotal * (form_irpf / 100)), 2)

        limpio = round((necesario - iva),2)
        context = {
            'necesario': necesario,
            'iva':iva,
            'subtotal':subtotal,
            'limpio' : limpio,
            'irpf':irpf
        }
        return render_template('index.html', **context)
    return render_template('index.html')


if __name__ == "__main__":
    # Esto es un problema porque no le podemos poner un puerto de salida, para eso vamos a crear lo siguiente:
        # SI HAY VARIABLE DE ENTORNO PORT COJE ESA VARIABLE, SI NO COJE EL 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)