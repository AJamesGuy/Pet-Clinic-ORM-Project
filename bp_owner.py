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
def update_owner(current_user):
    current_user.display()

    print("Fill in desired changes. To keep current values leave blank")
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    phone = input("Phone: ")


    if name:
        current_user.name = name
    if email:
        current_user.email = email
    if password:
        current_user.password = password
    if phone:
        current_user.phone = phone

    session.commit() # commit changes to the database
    print("----------------- Updated Info --------------")
    current_user.display()
    return current_user

#Update profile function
#Ask user to confirm they want to delete
#if so delete the current user from the session
#commits changes 
#call main() to start the program over

def delete_owner(current_owner):
    choice = input("To confirm you want to delete your account, type 'delete': ")
    if choice == 'delete':
        session.delete(current_owner)
        session.commit()
        print("Account deleted")
        return None
    else:
        print("You opted out, back to menu")
        return current_owner