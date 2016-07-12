# coding: utf-8

from sqlalchemy import func, distinct, desc

import pandas as pd
import numpy as np

import pytz
import time
from datetime import timedelta, datetime

from ticketdata.models import dbsession, Event, EventSnap, Listing
from ticketdata.helpers import add_events_to_listingtable, add_all_snaps



def time_last_snapped(gm_id):
    '''
    Queries the database for the last time we took a snapshot
    of the event info for this game.
    '''
    query = dbsession.query(EventSnap).filter(
        EventSnap.stubhub_id == gm_id).\
        order_by(desc(EventSnap.dt_acc))
    return query.first().dt_acc

def last_snaptime():
    '''
    Queries the database for the last time we took a snapshot
    of the event info for this game.
    '''
    return dbsession.query(EventSnap).order_by(
        desc(EventSnap.dt_acc)).first().dt_acc

def time_last_listed(gm_id):
    query = dbsession.query(Listing).filter(
        Listing.event_id == gm_id).\
        order_by(desc(Listing.dt_acc))
    return query.first().dt_acc

def time_until_game(gm_id):
    query = dbsession.query(Event.dt).filter(
        Event.stubhub_id == gm_id)
    return query.first().dt - datetime.utcnow()

def between_hours(h0,h1):
    t_now = datetime.utcnow()
    query = dbsession.query(Event).filter(
        Event.dt > t_now + timedelta(hours=h0)).filter(
        Event.dt < t_now + timedelta(hours=h1)).order_by(
        Event.dt)
    return [row.stubhub_id for row in query]

def between_days(d0,d1):
    t_now = datetime.utcnow()
    query = dbsession.query(Event).filter(
        Event.dt > t_now + timedelta(days=d0)).filter(
        Event.dt < t_now + timedelta(days=d1)).order_by(
        Event.dt)
    return [row.stubhub_id for row in query]

def after_days(d0):
    t_now = datetime.utcnow()
    query = dbsession.query(Event).filter(
        Event.dt > t_now + timedelta(days=d0)).order_by(
        Event.dt)
    return [row.stubhub_id for row in query]



def refresh_todos(wordy, force_overnight):
    if wordy != 'not':
        print 'Refreshing the to-do list of games...'
    t_now = datetime.utcnow()
    t_0 = time.time()
    hn = t_now.hour
    todo = []
    if (hn <3 or hn >= 11) or force_overnight:
        if t_now - last_snaptime() > timedelta(minutes=15):
            todo.append('snap')
            if wordy == 'very':
                print "we'll be snapping....",
        for gmid in between_hours(0,4):
            if time_last_listed(gmid) < t_now - timedelta(minutes=10):
                todo.append(gmid)
        for gmid in between_hours(4,12):
            if time_last_listed(gmid) < t_now - timedelta(minutes=20):
                todo.append(gmid)
        for gmid in between_hours(12,96):
            if time_last_listed(gmid) < t_now - timedelta(minutes=30):
                todo.append(gmid)
        for gmid in between_days(4,10):
            if time_last_listed(gmid) < t_now - timedelta(hours=4):
                todo.append(gmid)
        for gmid in between_days(10,30):
            if time_last_listed(gmid) < t_now - timedelta(hours=6):
                todo.append(gmid)
        for gmid in after_days(30):
            if time_last_listed(gmid) < t_now - timedelta(hours=10):
                todo.append(gmid)
    else:
        if t_now - last_snaptime() > timedelta(hours=5):
            todo.append('snap')
        for gmid in between_days(0,10):
            if time_last_listed(gmid) < t_now - timedelta(hours=8):
                todo.append(gmid)
        for gmid in between_days(10,24):
            if time_last_listed(gmid) < t_now - timedelta(hours=12):
                todo.append(gmid)
        for gmid in after_days(24):
            if time_last_listed(gmid) < t_now - timedelta(hours=18):
                todo.append(gmid)
    if wordy != 'not':
        print "Refreshment finished! Time elapsed: {} seconds.".format(
            round(time.time()-t_0))
        print "There are {} game ids to do.\n".format(len(todo))
        if wordy == 'very':
            if len(todo)>0 and todo[0]=='snap':
                print "Also have to snap, so",
                print "this should take about {} minutes.\n\n".format(
                    len(todo)/10 + 3)
            else:
                print "No snap necessary, so",
                print "this should take about {} minutes.\n\n".format(
                    len(todo)/10)
    return todo



def run_autoscrape(wordy, force_overnight):
    eastern = pytz.timezone('US/Eastern')
    acceptable = ['very', 'somewhat', 'not']
    if wordy not in acceptable:
        print "ERROR: Input must in {}.".format(acceptable)
        return
    print '\n\n{}Restarting ({}){}\n\n'.format(
        '-'*13,
        datetime.utcnow().replace(
            tzinfo=pytz.utc).astimezone(
            eastern).strftime("%X ET"),
        '-'*13)
    to_get = refresh_todos(wordy, force_overnight)
    try: 
        to_get.remove('snap')
        snapping = True
        num_games_to_list = min(len(to_get), 110)
    except:
        snapping = False
        num_games_to_list = min(len(to_get), 140)
    if snapping:
        print 'Snapping events... ({})'.format(
            datetime.utcnow()-timedelta(hours=4))
        w = add_all_snaps(wordy)
        if wordy != 'not':
            if w == 0:
                print "Error in snapping!"
            else:
                print 'Snapping complete!'
    query = dbsession.query(Event).filter(
        Event.stubhub_id.in_(
            to_get[:num_games_to_list])).order_by(
        Event.dt)
    if wordy != 'not':
        print 'Adding listings... ({})'.format(
            datetime.utcnow()-timedelta(hours=4))
    add_events_to_listingtable(
        query,
        datetime.utcnow().replace(tzinfo=pytz.utc), wordy)
    if wordy == 'very':
        print '\n'*5, '-'*20
    return 1


while True:
    run_autoscrape(wordy='somewhat', force_overnight = False)
