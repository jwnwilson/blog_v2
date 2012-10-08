from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blogV2.apps.data.models import Entry
from blogV2.apps.accounts.forms import BlogForm, RegisterForm, BlogManagerForm
from django.db.models import signals

import re

@login_required
def profile(request):
	try:
		profile = request.user.get_profile()
		ctx = {'profile': profile,
		'title': str(profile.user).title(),
		'email':str(profile.email)}
	except KeyError: 
		return redirect(reverse("accounts_register"))
	return render_to_response('profile.html',ctx,context_instance= RequestContext(request))
	
def register(request):
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save()
		user.backend = settings.AUTHENTICATION_BACKENDS[0]
		login(request, user)
		return redirect(reverse("accounts_profile"))
		
	ctx = {"form":form}
	return render_to_response("register.html",ctx, context_instance= RequestContext(request))

@login_required
def blogEntry(request,blog_id= None):
	print blog_id
	# New entry find unused pk
	pk = 1
	count = 1
	if blog_id == None:
		objs = Entry.objects.all()
		pk = (len(objs) + 1)
	else:
		pk= blog_id
	ctx = {}
	if request.method == "POST":
		blog_form = BlogForm(request.POST)
		if blog_form.is_valid():
			success = True
			title = blog_form.cleaned_data['title']
			text = blog_form.cleaned_data['text']
			#signals.message_sent.send(sender=BlogForm, title=ctx['title'])
			if blog_id:
				blogEntry = Entry.objects.get(pk= pk)
				blogEntry.text = text
				blogEntry.title = title
				blogEntry.save()
			else:
				blogEntry = Entry.objects.create(pk = pk,text = text,title = title, user = request.user.get_profile())
				blogEntry.save()
			return redirect(reverse("accounts_myBlog"))
		else:
			raise Error("blog form not valid")
	else:
		if blog_id:
			blogEntry = Entry.objects.get(pk= pk)
			blog_form = BlogForm(initial={'title': blogEntry.title, 'text': blogEntry.text})
		else:
			blog_form = BlogForm()
	ctx['blog_form'] = blog_form
	return render_to_response('blogEntry.html', ctx , context_instance= RequestContext(request))
	
@login_required
def myBlog(request):
	entries = Entry.objects.getUser_entries(request.user)
	paginator = Paginator(entries, 5)
	# get page number from url ?page=#
	page_num = request.GET.get('page',1)
	try:
		page = paginator.page(page_num)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		page = paginator.page(1)
	ctx = { 'page': page,
			'newID':1}
	return render_to_response('myblog.html', ctx , context_instance= RequestContext(request) )
	
@login_required
def blogManager(request):
	ctx = {}
	if request.method == "POST":
		blog_form = BlogManagerForm(request.user,request.POST)
		if blog_form.is_valid():
			submitType = request.POST.get('blogManagerSubmit')
			print submitType
			if submitType == 'delete_selected':
				# get selected entries
				selectedEntries = blog_form.clean_entryList(submitType)
				# delete from database
				print selectedEntries
				for entry in selectedEntries:
					#Entry.objects.filter(published=True)
					obj = Entry.objects.filter(title= entry)
					obj.delete()
				# return to database manager
				return redirect(reverse("accounts_blogManager"))
			elif submitType == 'edit_selected':
				existingEntry=None
				# get user entries
				entries = Entry.objects.getUser_entries(request.user)
				# find entry with matching title
				selectedEntryTitle = blog_form.clean_entryList(submitType)
				# get entry from database to populate default blog data
				for entry in entries:
					if entry and selectedEntryTitle:
						if entry.title == selectedEntryTitle[0]:
							existingEntry = entry
				# redirect to blog post
				return redirect(reverse("accounts_blogEntry", args=(existingEntry.pk, )))
				"""
				# get selected entry
				entries = Entry.objects.getUser_entries(request.user)
				selectedEntryTitle = blog_form.clean_entryList(submitType)
				if selectedEntryTitle:
					# get entry from database to populate default blog data
					for entry in entries:
						if entry:
							if entry.title == selectedEntryTitle[0]:
								existingEntry = entry
					blog_form = BlogForm(initial={'title': existingEntry.title, 'text': existingEntry.text})
					ctx['blog_form'] = blog_form
					return render_to_response('newBlogEntry.html', ctx , context_instance= RequestContext(request))"""
	
	blog_form = BlogManagerForm(request.user,request.POST)
	ctx = { 'blog_form': blog_form}
	return render_to_response('blogManager.html', ctx , context_instance= RequestContext(request) )
	
	

