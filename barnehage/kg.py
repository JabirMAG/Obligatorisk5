from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from kgmodel import (Foresatt, Barn, Soknad, Barnehage)
from kgcontroller import (form_to_object_soknad, insert_soknad, commit_all, select_alle_barnehager)
from svarfun import *

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY' # nødvendig for session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/barnehager')
def barnehager():
    information = select_alle_barnehager()
    return render_template('barnehager.html', data=information)

# Søknad lagring for Admin
soknader_lokalt = []


@app.route('/behandle', methods=['GET', 'POST'])
def behandle():
    if request.method == 'POST':
        sd = request.form  # Henter søknadsdata fra skjemaet
        soknader_lokalt.append(sd)
        # Henter ønsket barnehage fra foresatte (kan være tomt)
        ønsket_barnehage = sd.get('liste_over_barnehager_prioritert_5')
        
        # Bruk en funksjon for å sjekke ledig plass (finn_ledig_barnehage)
        valgt_barnehage = finn_ledig_barnehage(ønsket_barnehage)

        # Legg til informasjon om barnehageplass i søknadsdataene
        sd = sd.to_dict()
        sd['valgt_barnehage'] = valgt_barnehage

        # Lagre søknaden i databasen om nødvendig
        insert_soknad(form_to_object_soknad(sd))

        # Lagre dataene i session for visning på svar-siden
        session['information'] = sd

        return redirect(url_for('svar'))  # Omstyrer til svar-siden for visning av resultat
    else:
        return render_template('soknad.html')


@app.route('/svar')
def svar():
    information = session['information']
    return render_template('svar.html', data=information)


# Admin

@app.route('/commit')
def commit():
    commit_all()
    return render_template('commit.html')

@app.route('/soknader')
def adminsoknad():
    return render_template('adminsoknad.html', data=soknader_lokalt)

print("Script started")
import pandas as pd

# Testblokk, hadde problemer med å laste inn nettsiden og måtte se om at det var excel filen som ikke funket

try:
    kgdata = pd.ExcelFile(r'C:\Users\47939\Github\Obligatorisk5\barnehage\kgdata.xlsx')
    print("Excel file har lastet inn riktig")
except FileNotFoundError:
    print("Filen er ikke funnet")
except Exception as e:
    print(f"Feilmelding: {e}")


# For å runne flask :thumbs_up:
if __name__ == '__main__':
    app.run(debug=True)  # Starts the Flask server in debug mode

"""
Referanser
[1] https://stackoverflow.com/questions/21668481/difference-between-render-template-and-redirect
"""

"""
Søkeuttrykk

"""