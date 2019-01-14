# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import requests
import json
from xml.dom import minidom
from xml.dom.minidom import parse
import urllib.request
import re

username = ''


# ---- Main page for searching ----
def index():
    
    # Check url for vars
    search = ''
    if not request.vars:
        search = 'a'
    else:
        search = request.vars['starts_with']
        
    # Calling ann API
    req = ani_news_call(search)

    # Parse xml list
    listxml = minidom.parseString(req.text)
    info = listxml.getElementsByTagName('name')
    id = listxml.getElementsByTagName('id')
    
    # Add titles to the list
    #print('Item attribute:')  
    
    list1 = []
    list2 = []
    
    for i in info:
        for cn in i.childNodes:
            #print(cn.nodeValue)
            list1.append(cn.nodeValue)
            
    for i in id:
        for cn in i.childNodes:
            #print(cn.nodeValue)
            list2.append(cn.nodeValue)
                        
    #print(req.text)
    
    if len(list1) > 0:
        list1.pop(0)

    # Sort list1 while matching list2 elements
    lists = list(sorted(zip(list1,list2)))
    
    sorted_list1 = []
    sorted_list2 = []
    if len(lists) > 0:   
        sorted_list1, sorted_list2 = zip(*lists)
    
    return dict(message=(sorted_list1,sorted_list2))

# ---- Find anime by name ----
def ani_news_call(letter):
    list_params = {'id' : '155',
                   'type' : 'anime',
                   'name' : letter,
                   'nlist' : 'all'}
    
    req_list = requests.get("http://www.animenewsnetwork.com/encyclopedia/reports.xml?", params = list_params)
    return req_list

# ---- More info on selected anime ----
def viewer():
    
    # Check url for args
    search = ''
    if not request.vars:
        search = '1'
    else:
        search = request.vars['id']
    #print(request.args)
    
    req = ani_news_spec(search)
    
     # Parse xml list
    listxml = minidom.parseString(req.text)
    info1 = listxml.getElementsByTagName('anime')
    info2 = listxml.getElementsByTagName('info')
    info3 = listxml.getElementsByTagName('img')

    #print(req.text)
    print('-----------------------------')
    
    ani_name = ''
    ani_plot = ''
    ani_photo = ''
    
    # Search info, grab name, plot, image
    for i in info1:
        if(i.getAttribute('name') != ''):
            ani_name = i.getAttribute('name')
    
    for i in info2:
        if(i.getAttribute('type') == 'Plot Summary'):
            #print('plot here')
            for cn in i.childNodes:
                ani_plot = cn.nodeValue
        
    for i in info3:
        if(i.getAttribute('src') != ''):
            ani_photo = i.getAttribute('src')
    
    # Combine name, plot, image into list 
    ani_list = [ani_name, ani_plot, ani_photo, search]
    
    return dict(message=(ani_list))

def ani_news_spec(id):
    list_params = {'anime' : id}
    req_list = requests.get("https://cdn.animenewsnetwork.com/encyclopedia/api.xml?", params = list_params)
    return req_list

# search bar
def search_index():
    search = "index?starts_with=" + request.vars['search']
    redirect(URL('default', search))
    return dict(message=('search'))
    
def add_to_watch_list():
    
    q = (session.logged_in_user == db.watch_list.username) & (db.watch_list.anime_id == request.vars['id'])
    cl = db(q).select().first()

    # adds username, anime_id to watch list 
    if cl is None:
        db.watch_list.insert(
            username = session.logged_in_user,
            anime_id = request.vars['id'],
            anime_name = request.vars['title'],
            anime_picture = request.vars['photo']
        )
    
    redirect(URL('default', 'profile'))
    return

def remove_from_watch_list():
    #print(request.vars['id'])
    q = (session.logged_in_user == db.watch_list.username) & (db.watch_list.anime_id == request.vars['id'])
    cl = db(q).select().first()
    #print(cl)
    if cl is not None:
       db(q).delete()
    
    redirect(URL('default', 'profile'))
    return

# not used
def homepage():
    
    return dict(message=T("hi"))
    

def sign_up():
    #print(auth.user)
    return dict(message=T('Sign_up'))

# create a new account/login to existing account
def submit_sign_up():    
    
    q = (db.auth_user.email == request.vars.username)
    cl = db(q).select().first()

    if cl is None:
        # create account
        print('not found')
        db.auth_user.insert(
            first_name = None,
            last_name = None,
            email = request.vars.username,
            password = 'cheese'
        )
        print('added to db')
    
    check_user_table(request.vars.username)
    session.logged_in_user = request.vars.username
    
    #delete from table
    #db(db.auth_user.first_name == 'kernolkorn').delete()
    
    redirect(URL('default','index'))
    return dict(message=T('submitted'))

# adds user to table if needed
def check_user_table(user_name):
    q = (db.user_table.username == user_name)    
    cl = db(q).select().first()
    if cl is not None:
        # user already exists 
        print("a user with that name already exists")       
    else:
        # create new user
        db.user_table.insert(username=request.vars.username)
        username = request.vars.username
        print("added to table")
    return

# logs out of current account
def logout():
    session.logged_in_user = ''
    redirect(URL('default', 'index'))
    return

# profile page
def profile():
    watch_list_id = []
    watch_list_name = []
    watch_list_photo = []
    
    q = (session.logged_in_user == db.watch_list.username)
    cl = db(q).select()
    
    for row in cl:
        watch_list_id.append(row.anime_id)
        watch_list_name.append(row.anime_name)
        watch_list_photo.append(row.anime_picture)

    print(db(db.watch_list).select())    
    return dict(message=(watch_list_id, watch_list_name, watch_list_photo))

def paige():
    return dict(whatever=T('Im a Page'))

# searches youtube and returns url of first video
def youtube_trailer():

    search = request.vars.title
    search = search + " trailer anime"

    query = urllib.parse.quote(search)
    url = "https://www.youtube.com/results?search_query="+query
    response = urllib.request.urlopen(url)
    html = response.read()
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html.decode())

    url = "https://www.youtube.com/embed/" + search_results[0]
    print(url)
              
    return dict(message=T(url))


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
