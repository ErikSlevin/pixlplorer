# app/routes/setup_routes.py
from flask import render_template, redirect, url_for, flash
from app.forms import Step1Form, Step2Form  # Importiere die Formularklassen
from app.functions.setup_database import setup_database

from app import app

def setup_step1():
    form = Step1Form()
    if app.config['SETUP_COMPLETED']:
        flash("Das Setup wurde bereits abgeschlossen.", "danger")
        if form.validate_on_submit():
            return redirect(url_for('index'))
    else:
        if form.validate_on_submit():
            # Speichere die Daten des ersten Schritts
            return redirect(url_for('setup_step2'))  # Weiterleitung zum nächsten Schritt

    return render_template('setup_step1.html', form=form)

def setup_step2():
    form = Step2Form()

    if app.config['SETUP_COMPLETED']:
        flash("Das Setup wurde bereits abgeschlossen.", "danger")
        return redirect(url_for('index'))

    else:
        success, messages = setup_database()

        if success:
            for message in messages:
                flash(message, "success")
        else:
            for error in messages:
                flash(error, "danger")

        if form.validate_on_submit():
            print("SETUP_COMPLETED vor Setzen:", app.config['SETUP_COMPLETED'])
            app.config['SETUP_COMPLETED'] = True
            print("SETUP_COMPLETED nach Setzen:", app.config['SETUP_COMPLETED'])
   #        return redirect(url_for('index'))


    return render_template('setup_step2.html', form=form, messages=messages)


