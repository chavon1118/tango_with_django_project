from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'boldmessage': "This is the Index Page!",
		'categories': category_list, 
		'pages': page_list}

	
	# previous context dict for learning template
	# Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    # context_dict = {'boldmessage' : "This is the index page and I am bold because I'm important!"}
	
    # previous return before using the template
	# return HttpResponse("Rango says hey there the world!" + 
	# '<a href="/rango/about">About</a>')
	
	# Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
	return render(request, 'rango/index.html', context_dict)
    
	
def about(request):
    # Original return
	# return HttpResponse("Rango says here is the about page."
	# + '<a href="/rango/">Index</a>')
	context_dict = {'boldmessage' : "This is the About Page~"}
	return render(request, 'rango/about.html', context_dict)

def category(request,category_name_slug):
	# Create a context dictionary which we can pass to the template rendering engine
	context_dict = {}
	
	try:
		# Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
		pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
		context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
		context_dict['category'] = category
		
		context_dict['category_name_slug']=category.slug
	except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
		pass

    # Go render the response and return it to the client.
	return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		
		#Have we been provided with a valid form?
		if form.is_valid():
			#Save the new category to the database
			form.save(commit=True)
			
			#Now call the index() view
			# The user will be shown the homepage
			return index(request)
		else:
			#The supplied form contained errors - just print error
			print form.errors
	else:
		#If the request was not a POST, display the form to enter details
		form = CategoryForm()
	
	#Bad form (or form details), no form supplied...
	#Render the form with error messages(if any)
	return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):

	try:
		cat = Category.objects.get(slug=category_name_slug)
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
				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()
		
	context_dict = {'form': form, 'category' : cat}
	return render(request, 'rango/add_page.html', context_dict)
	
def register(request):

	registered = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			
			user.set_password(user.password)
			user.save()
			
			profile = profile_form.save(commit=False)
			profile.user = user
			
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			
			profile.save()
			registered = True
			
		else:
			print user_form.errors, profile_form.errors
	
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	
	return render(request,
			'rango/register.html',
			{'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
			

def user_login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse("Your Rango account is disabled.")
		
		else:
			print "Invalid login detals: {0}, {1}". format(username, password)
			return HttpResponse("Invalid login details supplied.")
	
	else:
		return render(request, 'rango/login.html', {})
		
@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')