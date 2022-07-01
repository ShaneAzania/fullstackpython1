from ast import Not, Try
from flask_app import app
from flask import flash, render_template,redirect,request,session
from flask_app.models.sighting import Sighting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

site_title = 'Sasquatch Websighting'

#Create Sightings
@app.route('/sighting_report')
def sighting_report():
    try:
        if int(session['user_id']):
            return render_template('sighting_report.html', title = site_title)
    except:
        return redirect('/register_login')
    
@app.route('/sighting_report_form', methods = ['POST'])
def sighting_report_form():
    data = {
        'location': request.form['location'],
        'description': request.form['description'],
        'date_of_sighting': request.form['date_of_sighting'],
        'number_sighted': request.form['number_sighted'],
        'user_id': session['user_id']
    }
    if Sighting.validate(data):
        Sighting.create(data)
        return redirect('/sightings_all')
    else:
        return redirect('/sighting_report')

#Retreive Sightings
@app.route('/sightings_all')
def sightings_all():
    try:
        if int(session['user_id']):
            return render_template('sightings_all.html', title = site_title, sightings = Sighting.get_all())
    except:
        return redirect('/')
@app.route('/sighting_view/<int:id>')
def sighting_view(id):
    sighting = Sighting.get_one({'id':id})
    return render_template('sighting_view.html', title = site_title, sighting = sighting)

#Update Sightings
@app.route('/sighting_edit/<int:id>')
def sighting_edit(id):
    return render_template('sighting_edit.html', title = site_title, sighting = Sighting.get_one({'id':id}))
@app.route('/sighting_edit_form', methods = ['POST'])
def sighting_edit_form():
    data = {
        'id': request.form['id'],
        'location': request.form['location'],
        'description': request.form['description'],
        'date_of_sighting': request.form['date_of_sighting'],
        'number_sighted': request.form['number_sighted']
    }
    if Sighting.validate(data):
        Sighting.update(data)
    else:
        return redirect('/sighting_edit/' + request.form['id'])
    return redirect('/sightings_all')

#Delet Sightings
@app.route('/sighting_delete/<int:id>')
def sighting_delete(id):
    Sighting.delete({'id':id})
    return redirect('/sightings_all')