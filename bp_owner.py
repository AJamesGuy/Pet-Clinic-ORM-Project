from models import Owners, session

#View profile function
#displays the current users info
def view_owner(current_user):
    print("Name: ", current_user.name)
    print("Email: ", current_user.email)
    print("Phone: ", current_user.phone)

#Update profile function
#displays current user info
#allows user to update any of the fields
#commits changes 
#shows changes and returns update current_user

#Update profile function
#Ask user to confirm they want to delete
#if so delete the current user from the session
#commits changes 
#call main() to start the program over