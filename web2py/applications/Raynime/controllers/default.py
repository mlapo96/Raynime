# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import requests
import json
import xml.etree.ElementTree as ET 
from xml.dom import minidom
from _winapi import NULL

# ---- example index page ----
def index():
    #response.flash = T("Hello World")
    #return dict(message=T('This is the help page!'))
    
    # Check url for args
    search = ''
    if not request.args:
        search = 'a'
    else:
        search = request.args[0]
    print(request.args)
        
    # Calling ann API
    req = ani_news_call(search)

    # Parse xml list
    listxml = minidom.parseString(req.text)
    #info = listxml.getElementsByTagName('name')
    #type = listxml.getElementsByTagName('type')
    info = listxml.getElementsByTagName('name')
    type = listxml.getElementsByTagName('type')
    
    # Add titles to the list
    print('Item attribute:')  
    
    list1 = []
    list2 = []
    
    for i in info:
        for cn in i.childNodes:
            print(cn.nodeValue)
            list1.append(cn.nodeValue)
            
    for i in type:
        for cn in i.childNodes:
            print(cn.nodeValue)
            list2.append(cn.nodeValue)
                        
    print(req.text)
    
    if len(list1) > 0:
        list1.pop(0)
    if len(list2) > 0: 
        list2.pop(0)
    list1.sort()
    print(list1)
    
    return dict(message=(list1))

def ani_news_call(letter):
    list_params = {'id' : '155',
                   'type' : 'anime',
                   'name' : letter,
                   'nlist' : 'all'}
    
    req_list = requests.get("http://www.animenewsnetwork.com/encyclopedia/reports.xml?", params = list_params)
    return req_list

def homepage():
    
    return dict(message=T("hi"))
    
def sign_up():
    return dict(message=T('Sign_up'))

def paige():
    return dict(whatever=T('Im a Page'))

def viewer():
    return dict(message=T('WAAAACHTER'))
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
