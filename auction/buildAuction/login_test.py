from hashlib import sha256
from .models import User
from .login import *

test_counter = 0
test_results = []

def get_pass_string(name):
    if name == None:
        return ("Test " + str(test_counter) + " finished succesfully")
    else:
        return (name + " finished succesfully")

def get_pass_obj(name):
    return (get_pass_string(name), True)

def get_fail_string(name):
    if name == None:
        return ("Test " + str(test_counter) + " failed")
    else:
        return (name + " failed")

def get_fail_obj(name):
    return (get_fail_string(name), False)

def test_create_user():
    name = "Bobo"
    password = "Boboblin"
    createUser(name, password)
    try:
        return User.objects.get(username=name)
    except:
        return None

def assert_true(arg,name=None):
    global test_counter
    test_counter += 1
    if arg == True:
        test_results.append(get_pass_obj(name))
    else:
        test_results.append(get_fail_obj(name))

def assert_false(arg,name=None):
    global test_counter
    test_counter += 1
    if arg == False:
        test_results.append(get_pass_obj(name))
    else:
        test_results.append(get_fail_obj(name))

def assert_None(arg,name=None):
    global test_counter
    test_counter += 1
    if arg == None:
        test_results.append(get_pass_obj(name))
    else:
        test_results.append(get_fail_obj(name))

def assert_not_None(arg,name=None):
    global test_counter
    test_counter += 1
    if arg != None:
        test_results.append(get_pass_obj(name))
    else:
        test_results.append(get_fail_obj(name))

def assert_equals(arg, test,name=None):
    global test_counter
    test_counter += 1
    if arg == test:
        test_results.append(get_pass_obj(name))
    else:
        test_results.append(get_fail_obj(name))


def print_report():
    print("------------------")
    print("---Test Results---")
    print("------------------")
    for i in test_results:
        print(("X"," ")[i[1]] + "\t" + i[0])

def run_tests():
    global test_results, test_counter
    test_counter = 0
    test_results = []
    user = test_create_user()
    user1= createUser("Bobo", "Password")
    assert_not_None(user, "User Created")
    assert_None(user1, "Copy User not Created")
    assert_true(checkPwd("Boboblin", user), "Password check 1")
    assert_false(checkPwd("qBoboblin", user), "Password check 2")
    user.delete()
    assert_None(getUser("Bobo"), "Verify user deletion")
    print_report()
