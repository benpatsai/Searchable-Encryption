from flask import g, render_template, request

from login import requirelogin
from zoodb import *
from debug import *
import bank_client
import traceback
import auth_client

@catch_err
@requirelogin
def transfer():
    warning = None
    try:
        if 'recipient' in request.form:
            if (request.form['zoobars']).isnumeric():
                zoobars = eval(request.form['zoobars'])
                commit = bank_client.transfer(g.user.person.username,
                          request.form['recipient'], zoobars, g.user.token)
                if commit:
                    warning = "Sent %d zoobars" % zoobars
                else :
                    raise ValueError
            else:
                raise ValueError()
    except (KeyError, ValueError, AttributeError) as e:
        traceback.print_exc()
        warning = "Transfer to %s failed" % request.form['recipient']

    return render_template('transfer.html', warning=warning)
