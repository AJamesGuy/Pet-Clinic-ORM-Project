#DONT FORGET TO IMPORT FUNCTIONS AFTER YOU MAKE THEM
from bp_auth import register, login
from models import Owners, session

def welcome_menu():
    current_user = None
    while True:
        print("""
--------- Welcome to Pet Clinic --------
        1.) Login
        2.) Register
""")
        choice = input("select (1 or 2) or quit: ")
        if choice == '1':
            current_user = login()
            return current_user

        elif choice == '2':
            current_user = register() # Owner object created and returned
            return current_user
        elif choice == 'quit':
            return
        else:
            print("Invalid response please try again.")

def owner_menu(current_user):
    while True:
        print("""
    1.) View Profile
    2.) Update Profile
    3.) Delete Profile
    4.) Back""")
        choice = input("choose 1-3: ")
        if choice == '1':
            #view profile function should display the current users info
            view_owner(current_user)
        elif choice == '2':
            #update profile function, and returns the updated user
            #on success, should set current_user to the user that is returned
            pass
        elif choice == '3':
            #delete the current users account
            pass
        elif choice == '4':
            return #Goes back to main menu
        else:
            print("Invalid Selection.")

def pets_menu(current_user):
    while True:
        print("""
1.) View my Pets
2.) Create Pet
3.) Update Pet
4.) Delete Pet
5.) Back""")
        choice = input("choose 1-5: ")
        if choice == '1':
            #function that displays the current user's pets
            pass
        elif choice == '2':
            #function to create a new pet linked to the current user, add to db
            pass
        elif choice == '3':
            #function to update a particular pet 
            pass
        elif choice == '4':
            #function to delete a particuler pet
            pass
        elif choice == '5':
            return
        else:
            print("Invalid Selection.")

def appointments_menu(current_user):
    while True:
        print("""
1.) schedule appointment
2.) view appointments
3.) reschedule appointment
4.) Complete appointment
5.) Back
""")
        choice = input("choose 1-5: ")
        if choice == '1':
            #Function to create a new appointment between one of the user's pets
            #and one of the vets
            pass
        elif choice == '2':
            #View current user's appointments
            pass
        elif choice == '3':
            #Reschedule appointment (change the date)
            pass
        elif choice == '4':
            #Complete appointment (change status to complete)
            pass
        elif choice =='5':
            return


def main():
    
    # current_user = welcome_menu() 

    #After you test you login and register functions, it might be more efficient
    #to set current_user to a user in your db so you don't have to log in everytime
    #you want to test something.
    
    current_user = session.get(Owners, 1)

    if current_user:
        while True:
            print("""
        --------- Pet Clinic --------
        1.) Manage Profile
        2.) My Pets
        3.) My Appointments
        """)
            choice = input("choose 1-3: ")
            if choice == '1':
                owner_menu(current_user)
            elif choice == '2':
                pets_menu(current_user)
            elif choice == '3':
                appointments_menu(current_user)
            else:
                print("Invalid Selection.")
    

main()
    
