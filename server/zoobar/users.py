from flask import g, render_template, request, Markup

from login import requirelogin
from zoodb import *
from debug import *
from profile import *
import bank_client
import profileDB_client
import message_client
import time

@catch_err
@requirelogin
def users():
    args = {}
    args['req_user'] = Markup(request.args.get('user', ''))
    args['post_msg'] = Markup(request.args.get('msg', ''))
    if 'user' in request.values:
        persondb = person_setup()
        user = persondb.query(Person).get(request.values['user'])
        if user:
            if 'msg' in request.values:
                message_client.new_message(g.user.person.username,request.values['user'],request.values['msg'])
            p = profileDB_client.get_profile(user.username)
            if p.startswith("#!python"):
                p = run_profile(user)

            p_markup = Markup("<b>%s</b>" % p)
            args['profile'] = p_markup

            args['user'] = user
            args['user_zoobars'] = bank_client.balance(user.username)
            args['transfers'] = bank_client.get_log(user.username)
        else:
            args['warning'] = "Cannot find that user."
    return render_template('users.html', **args)
