# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from qalearn.home.models import Document
from qalearn.home.forms import DocumentForm
import os
import json
import urllib.parse
import requests
from file2id import file2id
from sim2id import sim2id
import pickle as pkl
import re

def upper_repl(match):
	print(match.group(2).upper())
	return match.group(1) + match.group(2).upper()

def upload(request):
    # Handle file upload
	context = {}
	context['file_status'] = 0
	context['txt_status'] = 0
	context['data_status'] = 0

	form_status = 0
	doc_status = 0
	print("Requesting POST")

	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)

		if form.is_valid():
			print("form valid")
			doc_name,_ = os.path.splitext(request.FILES['docfile'].name)

			try:
				doc = Document.objects.get(name=doc_name)
				context['file_status'] = 1
				form = DocumentForm()  # A empty, unbound form
				print("object with same name")

			except:
				print("saving doc")
				context['file_status'] = 0
				data_name = doc_name + ".txt"
				newdoc = Document(docfile=request.FILES['docfile'], name=doc_name)
				newdoc.save()
				val = os.system("../pdfminer/tools/pdf2txt.py " + "media/documents/" + request.FILES['docfile'].name + " > media/txt/" + data_name)
				print(val)
				if(val == 0):
					print("txt converted")
					try:
						index_list, sections, flag = file2id("media/txt/" + data_name)

						if (flag!=1):
							print("sections saved")
							f = open("media/data/" + doc_name, "wb")
							pkl.dump([index_list, sections], f)
							f.close()

		            		# Redirect to the document list after POST
							return HttpResponseRedirect('/home/')				
						else:
							print("start > end error in sections")
							context['data_status'] = 1
							form_status = 1
							doc_status = 1
					except:
						print("error in extracted sections")
						context['data_status'] = 1
						form_status = 1
						doc_status = 1
				else:
					print("error in txt conversion")
					context['txt_status'] = 1
					form_status = 1
					doc_status = 1
	else:
		print("form not valid")
		form_status = 1
		# context['data_status'] = 0


	if(doc_status):
		doc = Document.objects.get(name=doc_name)
		doc.delete()

	if(form_status):
		form = DocumentForm()  # A empty, unbound form

	documents = Document.objects.all()
	context['documents'] = documents
	context['form'] = form
    # Render list page with the documents and the form
	print("form end")
	return render(
        request,
        'upload.html',
        context
    )

def index(request):
	context={}
	context['status1'] = None
	context['title_status1'] = None
	context['status2'] = None
	context['title_status2'] = None
	context['show'] = None
	context['file_select_status'] = 0
	context['no_ans_status'] = 0
	context['more'] = 0

	num_ans = 1
	ans = ""
	url = "http://allgood.cs.washington.edu:1995/submit?paragraph="
	para = 'The Normans (Norman: Nourmands; French: Normands; Latin: Normanni) were the people who in the 10th and 11th centuries gave their name to Normandy, a region in France. They were descended from Norse ("Norman" comes from "Norseman") raiders and pirates from Denmark, Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles III of West Francia. Through generations of assimilation and mixing with the native Frankish and Roman-Gaulish populations, their descendants would gradually merge with the Carolingian-based cultures of West Francia. The distinct cultural and ethnic identity of the Normans emerged initially in the first half of the 10th century, and it continued to evolve over the succeeding centuries.'
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	headers={'User-Agent':user_agent,}

	try:
		documents = Document.objects.all()
		context['documents'] = documents
	except:
		print("no doc")
		context['documents'] = None
		
	print("Requesting GET")		
	if(request.method == 'GET'):
		ques = request.GET.get('question')
		file = request.GET.get('file')
		print("Ques:", ques)
		print("File:", file)

		if file not in ["Choose a file", None]:
			print("preview of pdf")
			context['file'] = file
			context['show'] = 1

		if (file not in ["Choose a file", None]):
			if (ques  not in ["", None]):
				
				print("loading data")
				f = open("media/data/" + file, "rb")
				index_list, sections = pkl.load(f)
				f.close()
				print("calculating similarity")
				top_ids, top_sims,top_titles, top_n_ids = sim2id(num_ans, sections, index_list, ques)

				for i in range(num_ans):
					if(top_sims[i]):
						try:
							print("sending data to bidaf")
							final_url = url+urllib.parse.quote_plus(sections[top_ids[i]])+"&question="+urllib.parse.quote_plus(ques.lower())
							print("url", final_url)
							url_request = urllib.request.Request(final_url,None,headers)
							response = urllib.request.urlopen(url_request)
							data = response.read()
							json_data = json.loads(data.decode())
							try:
								print("retriving answer")
								ans_data = json_data['result']
								if(ans_data != ""):
									print("answer found")
									ans_data = re.sub("\n+", " ", ans_data)
									ans +=  ans_data.capitalize()
									ans = re.sub("(.[\.?]\s+)(\w)", upper_repl, ans)
									context['status'+str(i+1)] = 1
									context['title_status'+str(i+1)] = 1
									context['answer'+str(i+1)] = ans
									context["ques"] = ques
									context["title"+str(i+1)] =  top_n_ids[i] + "    " + top_titles[i].upper()
								else:
									context["ques"] = ques
									context['title_status'+str(i+1)] = 1
									context["title"+str(i+1)] =  top_n_ids[i] + "    " + top_titles[i].upper()

							except:
								print("no answer")
								context['no_ans_status'] = 1
								context["ques"] = ques
						except:
							print("internet down")
					else:
						print("no answer")
						context['no_ans_status'] = 1
						context["ques"] = ques
		else:
			context['file_select_status'] = 1

	print("end of index")
	return render(request, 'home.html', context)