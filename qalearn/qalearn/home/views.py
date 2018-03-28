# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from qalearn.home.models import Document
from qalearn.home.forms import DocumentForm

import json
import urllib.parse
import requests

def upload(request):
    # Handle file upload
	context = {}
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile=request.FILES['docfile'])
			newdoc.save()

            # Redirect to the document list after POST
			return HttpResponseRedirect(reverse('upload'))
	else:
		form = DocumentForm()  # A empty, unbound form

	documents = Document.objects.all()
	context['documents'] = documents
	context['form'] = form
    # Render list page with the documents and the form
	return render(
        request,
        'upload.html',
        context
    )

def index(request):
	context={}
	context['status'] = None
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
	if(request.method == 'GET'):
	    print("data")
	    ques = request.GET.get('question')
	    file = request.GET.get('file')
	    print(ques)
	    print(file)

	    context['file'] = file
	    if(ques  !=""):
	        try:
	            print("trying")
	            final_url = url+urllib.parse.quote_plus(para)+"&question="+urllib.parse.quote_plus(ques)
	            url_request = urllib.request.Request(final_url,None,headers)
	            response = urllib.request.urlopen(url_request)
	            data = response.read()
	            json_data = json.loads(data.decode())
	            try:
	                ans = json_data['result']
	                context['status'] = 1
	                context['answer'] = ans
	                context["ques"] = ques
	            except:
	                print("no answer")
	        except:
	            print("internet down")

	return render(request, 'home.html', context)