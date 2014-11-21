from __future__ import absolute_import

from flask import url_for


def static_helper(filename):
    # TODO support CDNs
    return url_for('static', filename=filename)
