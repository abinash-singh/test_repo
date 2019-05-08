from django.shortcuts import render
import requests
import json
from pymongo import MongoClient
import sys, traceback
from .models import inVoidUsers
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404
from bson.json_util import dumps
from .methods import obj_to_list
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
# Create your views here.

test = 10

client = MongoClient("mongodb+srv://abinash-singh:gayatree%40123@cluster0-t2gln.mongodb.net/test?retryWrites=true")
#client = MongoClient('mongodb+srv://invoid:invoid1404@invoid-9snlk.mongodb.net/test?retryWrites=true')
mongodb = client.video_kyc_demo
face_verification_obj = mongodb.face_verification

def login(request):

	# Code for restore last session if user has not logout
	try:
		if request.session['authkey'] == "superuser":
			context = request.session['context']
			template_name = "login/superuser.html"
			return render(request, template_name, context)
		if request.session['authkey'] != "":
			context = request.session['context']
			template_name = "login/details.html"
			return render(request, template_name, context)
	except:
		pass

	######################################################

	template_name = "login/login.html"

	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')

		if not username:
			context = {'message' : "Please provide username"}
			return render(request, template_name, context)
		if not password:
			context = {'message' : "Please provide password"}
			return render(request, template_name, context)
		try:
			if inVoidUsers.objects.filter(username = username):
				logged_user = get_object_or_404(inVoidUsers, username=username, password=password)					

			else:
				context = {'message' : "Invalid Crediantial"}
				return render(request, template_name, context)
			

			if logged_user:

				data = face_verification_obj.find({'auth_key' : logged_user.authkey})
				serialized = dumps(data)
				dict_data = json.loads(serialized)

				temp = obj_to_list(dict_data)
				context = {'message' : temp}

				request.session['authkey'] = logged_user.authkey
				request.session['context'] = context

				template_name = "login/details.html"
				return render(request, template_name, context)


			else:
				context = {'message' : "User does not exist."}
				return render(request, template_name, context)

		except Exception as err:
			traceback.print_exc(file=sys.stdout)
			context = {'message' : "Something wrong"}
			return render(request, template_name, context)
		
		return render(request, template_name)

	return render(request, template_name)

def details(request):
	try:
		if request.session['authkey'] != "":
			context = request.session['context']
			template_name = "login/details.html"
			return render(request, template_name, context)
	except:
		pass
	template_name = "login/logout.html"
	return render(request, template_name, {'message' : 'Login required!'})	


def logout(request):
	request.session['authkey'] = ""
	request.session['context'] = ""
	template_name = "login/logout.html"

	return render(request, template_name)

