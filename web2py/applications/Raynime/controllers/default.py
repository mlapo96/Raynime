# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import requests
import json
import xml.etree.ElementTree as ET 
from xml.dom import minidom

# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('This is the help page!'))

def homepage():
    # Make a get request to get the latest position of the international space station from the opennotify api.
  
    param = {'anime' : '87'}
    list_params = {'type' : 'anime', 
                   'name' : 'Z',
                   'nskip' : '0',
                   'nlist' : '8'}
     
    req = requests.get("http://cdn.animenewsnetwork.com/encyclopedia/api.xml", params=param)
    print(req.url)
    
    
    req_list = requests.get("http://cdn.animenewsnetwork.com/encyclopedia/api.xml", params=list_params)

    print(type(req))

    
    # Parsing the xml
    myxml = minidom.parseString(req.text)
    basic_info = myxml.getElementsByTagName('anime')
    items_2 = myxml.getElementsByTagName('info')
    
    list = [ basic_info[0].attributes['name'].value, items_2[0].attributes['src'].value ]
    
    print('Item attribute:')  
    
    for item in list:
        print(item)

    
    myxml_2 = minidom.parseString(req_list.text)
    info = myxml_2.getElementsByTagName('anime')
    print(myxml_2.)
    
    return dict(message=(list))

def sign_up():
    return dict(message=T('Sign_up'))

def paige():
    return dict(whatever=T('Im a Paige'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
