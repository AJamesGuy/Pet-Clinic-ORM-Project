from models import Owners, session #Need the Users model to create and search for users
#need the session to add users to our db



#Create Login function
#get email and password from user
#check database for owner with the given email
#if you find an owner, check if the found owners password is the same as the given password
#if so return user
def login():
    print("---------------")
    email = input("Email: ")
    password = input("Password: ")

    user = session.query(Owners).where(Owners.email == email).first() #Searching our Owners table for a user with the provided email
    
    if user and user.password == password:
        print("Successfully logged in")
        print(f"Welcome back {user.name}")
        return user
    else:
        print("Invalid username or password.")


#Create Register function
#get all info required to create an owner from the user
#try and create an Owner from the info (will fail if email is already in user)
#if you succeed return user
#except error and print message

def register():
    print("----------------- Welcome! Please fill in the following to register -----------------")
    
    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    password = input("Password: ")

    try:
        new_owner = Owners(name=name, email=email, phone=phone, password=password)
        session.add(new_owner)
        session.commit()
        print(f"Welcome {name}!")
        return new_owner
    except Exception as e:
        print("Issue creating this account", e)