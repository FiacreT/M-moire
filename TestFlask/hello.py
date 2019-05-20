#/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def racine():
    return "Le chemin de 'racine' est : " + request.path

@app.route('/la')
def ici():
    return "Le chemin de 'ici' est : " + request.path


if __name__ == '__main__':
    app.run()

