from models import Owner, session

#View profile function
#displays the current users info
def view_owner(current_user):
    print("Name:", current_user.name)
    print("Email:", current_user.email)
    print("Phone:", current_user.phone)
    print("Member ID:", current_user.id)
    print("Total Pets:", len(current_user.pets))
    print("="*50)

#Update profile function
#displays current user info
#allows user to update any of the fields
#commits changes 
#shows changes and returns update current_user
def update_owner(current_user):
    current_user.display()

    print("Leave blank to keep current value.")
    name = input(f"New name [{current_user.name}]: ").strip()
    email = input(f"New email [{current_user.email}]: ").strip()
    password = input("New password [********]: ").strip()
    phone = input(f"New phone [{current_user.phone}]: ").strip()

    try:
        if name:
            current_user.name = name
        if email:
            exists = session.query(Owner).where(Owner.email == email).first()
            if exists:
                print("This email is already taken!")
                return current_user
            current_user.email = email
        if password:
            if len(password) < 6:
                print("Password must be at least 6 characters!")
                return current_user
            current_user.password = password
        if phone:
            current_user.phone = phone

        session.commit() # commit changes to the database
        print("----------------- Updated Info --------------")
        current_user.display()
        return current_user
    except Exception as e:
        print("An error occurred while updating profile:", e)
        return current_user

#Delete profile function
#Ask user to confirm they want to delete
#if so delete the current user from the session
#commits changes 
#call main() to start the program over

def delete_owner(current_owner):
    print("WARNING: THIS WILL PERMANENTLY DELETE YOUR ACCOUNT AND ALL PETS!")
    confirm = input("Type 'DELETE MY ACCOUNT' to confirm: ").strip()
    if confirm != "DELETE MY ACCOUNT":
        print("Account deletion cancelled.")
        return current_owner
    try:
        session.delete(current_owner)
        session.commit()
        print("Account deleted")
        return None
    except Exception as e:
        print("An error occurred while deleting account:", e)
        return current_owner