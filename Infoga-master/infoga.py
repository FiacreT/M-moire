#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#
# @name   : Infoga - Email OSINT
# @url    : http://github.com/m4ll0k
# @author : Momo Outaadi (m4ll0k)

import sys
import json
import getopt
# infoga.lib
from lib.check import *
from lib.output import *
from lib.banner import Banner
# infoga.recon
from recon.ask import *
from recon.baidu import *
from recon.bing import *
from recon.pgp import *
from recon.yahoo import *
from recon.dogpile import *
from recon.exalead import *
from recon.google import *
from recon.mailtester import *
from lib.output import PPrint
import re

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

class Infoga(Resource, object):
	""" infoga """
	def __init__(self):
		self.verbose = 1
		self.domain = None
		self.breach = False
		self.source = "all"
		self.listEmail = []
		self.report = None

	def search(self,module):
		emails = module.search()
		if emails != ([] or None):
			for email in emails:
				if email not in self.listEmail:
					self.listEmail.append(email)
			if self.verbose in (1,2,3):
				info('Found %s emails in %s'%(len(emails),
					module.__class__.__name__))

	def engine(self,target,engine):
		engine_list = [ Ask(target),Baidu(target),Bing(target),Dogpile(target),
						Exalead(target),Google(target),PGP(target),Yahoo(target)
						]
		if engine == 'all':
			for e in engine_list: self.search(e)
		else:
			for e in engine_list:
				if e.__class__.__name__.lower() in engine:self.search(e)

	def tester(self,email):
		return MailTester(email).search()

	def post(self, target):
		#if len(sys.argv) <= 2:Banner().usage(True)
		try:
			'''opts,args = getopt.getopt(sys.argv[1:],'d:s:i:v:r:hb',
				['domain=','source=','info=','breach','verbose=','help','report='])'''
			print("-----------------------------------------------------------------------")
			
			#opts.clear()
			opts = []
			opts.append(('--info', target))
			opts.append(('-s', 'all'))
			opts.append(('--breach', ''))
			opts.append(('-v', '3'))
			opts.append(('--report', 'result.txt'))
			#[('--info', 'fiacresoubgui@yahoo.fr'), ('-s', 'all'), ('--breach', ''), ('-v', '3'), ('--report', 'result.txt')]
			print(opts)

		except Exception as e:
			Banner().usage(True)
		Banner().banner()
		for o,a in opts:
			if o in ('-d','--domain'):self.domain=checkTarget(a)
			if o in ('-v','--verbose'):self.verbose=checkVerbose(a)
			if o in ('-s','--source'):self.source=checkSource(a)
			if o in ('-b','--breach'):self.breach=True
			if o in ('-r','--report'):self.report= open(a,'wb') if a != '' else None
			if o in ('-i','--info'):
				self.listEmail.append(checkEmail(a))
				plus('Searching for: %s'%a)
			if o in ('-h','--help'):Banner().usage(True)
		### start ####
		if self.domain != ('' or None):
			if self.source == 'ask':self.engine(self.domain,'ask')
			if self.source == 'all':self.engine(self.domain,'all')
			if self.source == 'google':self.engine(self.domain,'google')
			if self.source == 'baidu':self.engine(self.domain,'baidu')
			if self.source == 'bing':self.engine(self.domain,'bing')
			if self.source == 'dogpile':self.engine(self.domain,'dogpile')
			if self.source == 'exalead':self.engine(self.domain,'exalead')
			if self.source == 'pgp':self.engine(self.domain,'pgp')
			if self.source == 'yahoo':self.engine(self.domain,'yahoo')

		if self.listEmail == [] or self.listEmail == None:
			sys.exit(warn('Not found emails... :(')) 
		
		for email in self.listEmail:
			ip = self.tester(email)
			if ip != ([] or None):
				ips = []
				for i in ip:
					if i not in ips:ips.append(i)
				if len(ips) >=2:
					info("Found multiple ip for this email...")
				PPrint(ips,email,self.verbose,self.breach,self.report).output()
			else:more('Not found any informations for %s'%(email))
		if self.report != None:
			info('File saved in: '+self.report.name)
			self.report.close()
		return target, 201
		# end
	
	def get(self, target):
		result = []
		info = ""
		leaked = ""
		with open("result.txt") as f:
			result = f.readlines()

		for i in range(len(result)):
			result[i] = result[i].replace("\n", "")
			if i!=0:
				info = info + result[i] + " "
			
			indice = info.find('>>')
			leaked = info[indice:]
			leaked = leaked.replace(">>", "")
			info = info.replace(leaked, "")

		
		results = {
            "target" : target,
            "info" : info,
			"leaked": leaked
		}
		return results, 200

if __name__ == "__main__":

	try:
		#infoga().main()
		api.add_resource(Infoga, "/infoga/<string:target>")
		app.run(debug=True, port=5008, threaded=True)
	except KeyboardInterrupt as e:
		sys.exit(warn('Exiting...'))