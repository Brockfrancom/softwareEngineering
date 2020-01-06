from hashlib import sha256
from .models import User
from .models import Access

def hashword(pswd, user):
	pwd = pswd + user.username
	hsh = sha256(pwd.encode()).hexdigest()
	return hsh

def getUser(uname):
	bob = None
	try:
		bob = User.objects.get(username=uname)
	except:
		return bob
	return bob

def setPwd(pswd, user):
	user.password_hashed = hashword(pswd, user)
	user.save()

def checkPwd(pswd, user):
	return hashword(pswd, user) == user.password_hashed

def createUser(username, pswd, name, email, admin=False):
	if len(User.objects.filter(username=username)) > 0:
		return None
	bob = User()
	bob.username = username
	bob.fullName = name
	bob.email = email
	setPwd(pswd, bob)
	bob.save()
	access = Access()
	access.user = bob
	access.admin_level = False
	if (admin):
		access.admin_level = True
	access.save()
	return bob

def checkAdmin(username):
	try:
		bob = User.objects.get(username=username)
		acs = Access.objects.get(user=bob.id)
		return acs.admin_level
	except:
		return False

def login(username, password, request):
	try:
		bob = User.objects.get(username=username)
		if (checkPwd(password, bob)):
			request.session["logged"] = True;
			request.session["username"] = username;
			request.session["uid"] = bob.id;
			request.session.set_expiry(600)
			return True
		else:
			return False
	except:
		return False

def delete_all_user():
    User.objects.all().delete()

def create_gill_bates():
	createUser("Blimo", "iluvscrum", "Blake Imons", "blimo@gmail.com")
	return createUser("GillBates", "nomber", "Gill Bates", "gill.bates@mircofost.com", True)

def login_init():
    delete_all_user()
    return create_gill_bates()
