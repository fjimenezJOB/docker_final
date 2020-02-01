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
        # Datos del Formulario
        form_total = round(float(request.form.get('necesario')), 2)
        form_iva = round(float(request.form.get('iva')), 2)
        form_irpf = round(float(request.form.get('irpf')), 2)

        # Calculos intermedios
        cal01 = ((form_iva - form_irpf) / 100) + 1
        cal02 = form_total / cal01

        # Calculos finales
        irpf = round((cal02 * (form_irpf / 100)), 2)
        iva = round((cal02 * (form_iva / 100)), 2)

        subtotal = round(cal02, 2)
        limpio = round(form_total - iva, 2)

        context = {
            'necesario': form_total,
            'iva': iva,
            'subtotal': subtotal,
            'limpio': limpio,
            'irpf': irpf
        }

        return render_template('index.html', **context)
    return render_template('index.html')


if __name__ == "__main__":
    # Esto es un problema porque no le podemos poner un puerto de salida, para eso vamos a crear lo siguiente:
    # SI HAY VARIABLE DE ENTORNO PORT COJE ESA VARIABLE, SI NO COJE EL 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
