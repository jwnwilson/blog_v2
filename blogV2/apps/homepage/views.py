from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import backend, connections
from django.db.models.aggregates import Count
from blogV2.apps.data.models import Entry
from blogV2 import settings

import os, sys
import datetime

def getDataFile(fileName):
	# get intro text
	filePath = (settings.STATIC_ROOT + "/data/" + fileName)
	if os.path.isfile(filePath):
		File = open(filePath)
		introText = File.read()
		File.close()
	else:
		introText = ''
	return introText

def index(request):
	entries = Entry.objects.published_entries()
	paginator = Paginator(entries, 5)
	
	# get page number from url ?page=#
	page_num = request.GET.get('page',1)
	try:
		page = paginator.page(page_num)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		page = paginator.page(1)
		
	# get intro text
	introText = getDataFile("blog_introText.txt")
		
	ctx = { 'page': page,
		'introText':introText}
	return render_to_response('index.html', ctx , context_instance= RequestContext(request) )
	
def archive(request, month = None):
	
	base_qs = Entry.objects.published_entries()
	in_archive_count = base_qs.count()
	page = None
	
	if month == None:
		month = backend.DatabaseOperations(connections).date_trunc_sql('month','created')
		per_month_count = base_qs.extra({'date':month}).values('date').annotate(count=Count('pk')).order_by('date')
		month = ''
		year = ''
	else:
		per_month_count = []
		today = datetime.datetime.today()
		year = today.year
		entries = base_qs.filter(created__year=today.year,created__month=today.month)
		paginator = Paginator(entries, 5)
	
		# get page number from url ?page=#
		page_num = request.GET.get('page',1)
		try:
			page = paginator.page(page_num)
		except EmptyPage:
			page = paginator.page(paginator.num_pages)
		except PageNotAnInteger:
			page = paginator.page(1)
	
	ctx = {'page': page,
		'month':month,
		'year':year,
		"in_archive_count": in_archive_count,
		"per_month_count": per_month_count,
	}
	return render_to_response('archive.html', ctx, context_instance= RequestContext(request))
	
def about(request):
	# get about text
	aboutText = getDataFile("blog_aboutText.txt")
	ctx = { 'aboutText':aboutText}
	return render_to_response('about.html', ctx ,context_instance= RequestContext(request))
	

