from sqlite3 import dbapi2
from unittest import result
from flask import flash
from flask_app.assets.regex import EMAIL_REGEX
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Sighting:
    db = 'sasquatch_websighting'
    db_table = 'sightings'
    db_table_sndry = 'users'
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.location = db_data['location']
        self.description = db_data['description']
        self.date_of_sighting = db_data['date_of_sighting']
        self.number_sighted = db_data['number_sighted']
        self.user_id = db_data['user_id']
        self.creator = None
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
    # **********************************************************************************************************************************
    # create*****************************************************************
    @classmethod
    def create( cls , data ):
        query = "INSERT INTO " + cls.db_table + " ( location, description, date_of_sighting, number_sighted, user_id ) VALUES ( %(location)s, %(description)s, %(date_of_sighting)s, %(number_sighted)s, %(user_id)s );"
        return connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #retreive*****************************************************************
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM " + cls.db_table + " LEFT JOIN " + cls.db_table_sndry + " ON " + cls.db_table + ".user_id = " + cls.db_table_sndry + ".id;"
        results =  connectToMySQL(cls.db).query_db(query)
        sightings =[]
        for x in results:
            sighting = cls(x)
            sighting.creator = user.User.get_one({'id':x['user_id']})
            sightings.append(sighting)
        return sightings
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM " + cls.db_table + " LEFT JOIN " + cls.db_table_sndry + " ON " + cls.db_table + ".user_id = " + cls.db_table_sndry + ".id WHERE " + cls.db_table + ".id = %(id)s;"
        results =  connectToMySQL(cls.db).query_db(query,data)
        sighting = cls(results[0])
        sighting.creator = user.User.get_one({'id':results[0]['user_id']})
        return sighting
    #**********************************************************************************************************************************
    #update*****************************************************************
    @classmethod
    def update(cls,data):
        query = "UPDATE "+ cls.db_table +" SET location = %(location)s, description = %(description)s, date_of_sighting = %(date_of_sighting)s, number_sighted = %(number_sighted)s, updated_at = now() WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #delete*****************************************************************
    @classmethod
    def delete (cls, data):
        query = "DELETE FROM " + cls.db_table + " WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db( query, data)

    def validate(data):
        valid = True
        if len(data['location']) < 2:
            valid = False
            flash('Please enter a valid location.')
        if len(data['description']) < 10 or len(data['description']) > 255:
            valid = False
            flash('Please give a description between 10 and 255 characters.')
        if not data['date_of_sighting']:
            valid = False
            flash('Please select a date.')
        if int(data['number_sighted']) < 1:
            valid = False
            flash('Select Sasquatch quantity of at least 1 or more.')
        return valid


