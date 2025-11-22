from models import Owner, session #Need the Users model to create and search for users
#need the session to add users to our db



#Create Login function
#get email and password from user
#check database for owner with the given email
#if you find an owner, check if the found owners password is the same as the given password
#if so return user
def login():
    print("\n" + "="*50)
    print("LOGIN")
    print("="*50)
    
    email = input("Email: ").strip()
    password = input("Password: ")

    try:
        user = session.query(Owner).where(Owner.email == email).first() #Searching our Owners table for a user with the provided email

        if user and user.password == password:
            print(f"\nSuccessfully logged in! Welcome back {user.name}!")
            return user
        else:
            print("Invalid username or password.")
            return None
    except Exception as e:
        print("An error occurred during login:", e)
        return None


#Create Register function
#get all info required to create an owner from the user
#try and create an Owner from the info (will fail if email is already in user)
#if you succeed return user
#except error and print message

def register():
    print("----------------- Welcome! Please fill in the following to register -----------------")
    
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    password = input("Password: ").strip()

    if len(password) < 6:
        print("Password must be at least 6 characters!")
        return None

    try:
        exists = session.query(Owner).where(Owner.email == email).first()
        if exists:
            print("An account with this email already exists.")
            return None

        new_owner = Owner(name=name, email=email, phone=phone, password=password)
        session.add(new_owner)
        session.commit()
        session.refresh(new_owner)

        print(f"Account created successfully! Welcome, {name}!")
        return new_owner
    
    except Exception as e:
        print(f"Failed to create account: {e}")
        return None