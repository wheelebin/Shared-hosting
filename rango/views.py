import random, string
from django.shortcuts import render, HttpResponse
from rango.models import Category, Page, Plan, UserProfile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from rango.forms import CategoryForm, PageForm, Planform, UserForm, UserProfileForm
from rango.hosting_backend.backend import fix_files, Handle_dns

def index(request):
	category_list = Category.objects.all()
	pages = Page.objects.order_by('-views')[:5]
	return render(request, 'rango/index.html', {
												'categories':category_list,
												'pages':pages
												})

def about(request):
	boldMsg = "World"
	return render(request, 'rango/about.html', {
												'boldMsg':boldMsg
												})

def category(request,  category_slug):
	try:
		#Get category from slug, category name and pages that belong to it
		category = Category.objects.get(slug=category_slug)
		category_name = category.name
		pages = Page.objects.filter(category=category)

	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html', {
													'category':category,
													'category_name':category_name,
													'pages':pages
													})

@login_required
def add_category(request):
	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()

	return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_slug):

    try:
        cat = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {
    												'form':form, 
    												'category': cat
    												})

@login_required
def add_domain(request):
	error = None

	#Check if user has an ftp account on server
	userprofile = UserProfile.objects.filter(user=request.user)
	if userprofile[0].ftp == 0:
		ranPass = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(10))
	else:
		ranPass = None

	if request.method == "POST":
		form = Planform(request.POST)
		if form.is_valid():
			plan = form.save(commit=False)
			plan.owner = request.user
			plan.directory = "/home/%s/%s/html/" % (request.user, request.POST.get('domain', ""),)
			plan.domain = request.POST.get('domain', "")
			plan.save()

			if len(plan.domain.split(".")) == 2:

				if Handle_dns(plan.domain, "domains").create_domain():
					error = "An error occured when attempting to create domain files"
					print error
				else:
					if Handle_dns(plan.domain, "records").create_records():
						error = "An error occured when attempting to create record files"
					else:
						fix_files(plan.directory, plan.domain, plan.owner).create_folder()
						fix_files(plan.directory, plan.domain, plan.owner).add_sftp_user(ranPass)
						profile = UserProfile.objects.get(user=request.user)
						profile.ftp = 1
						profile.save()

						if ranPass == None:
							return index(request)
						else:
							paswd = "Your FTP password is %s. This will only be displayed once so SAVE IT!!" % ranPass
							goBack = "<br><a href='/manage'>Go to manager</a>"
							return HttpResponse(paswd+goBack)
			else:
				error = "Please only use domain name and domain extension. Example: example.com"
		else:
			print form.errors
	else:
		form = Planform()

	return render(request, 'rango/add_domain.html', {
													'form': form,
													'error':error,
													})


@login_required
def manage_domain(request):
	current_user = request.user.id
	error = None
	try:
		plans = Plan.objects.filter(owner=current_user)
	except Plan.DoesNotExist:
		plans = None

	if request.method == "POST":
		form = Planform(request.POST)
		if form.is_valid():
			error = "The domain " + request.POST.get('domain', "") + " can't be deleted since it's not registered!"
			
		else:
			plan = Plan.objects.get(domain=request.POST.get('domain', ""))
			if plan.owner.id == current_user:
				plan.owner = request.user
				plan.directory = "/home/%s/%s"  % (request.user, request.POST.get('domain', ""),)
				plan.domain = request.POST.get('domain', "")

				fix_files(plan.directory, plan.domain, plan.owner).delete_domain()
				Handle_dns(plan.domain, "del").del_domain()
				plan.delete()

				return index(request)
	else:
		form = Planform()

	return render(request, 'rango/manage.html', {
														'form': form,
														'current_user':current_user,
														'plans':plans,
														'error':error,
														'username':request.user,
														})


def register(request):
	registered = False

	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():

			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			profile.ftp = 0
			profile.save()
			registered = True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'rango/register.html', {
	 												'user_form': user_form,
	 												'profile_form':profile_form,
	 												'registered': registered
	 												})

def user_login(request):

	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(username=username, password=password)

		#If info was correct
		if user:
			#Is user active?
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("You're account is disabled")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Your account is disabled")

	else:
		return render(request, 'rango/login.html', {})

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

#Make sure this only does it once a day!
@login_required
def reset_ftp_password(request):
	ranPass = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(10))
	fix_files(None, None, request.user).reset_ftp_pass(ranPass)
	paswd = "Your FTP password is %s. This will only be displayed once so SAVE IT!!" % ranPass
	goBack = "<br><a href='/manage'>Go to manager</a>"
	return HttpResponse(paswd+goBack)