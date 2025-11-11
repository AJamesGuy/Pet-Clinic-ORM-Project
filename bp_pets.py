from models import Pets, session

#view pets function
#Takes in current user
#Loops over all of the current users pets (use the .pets relationship attribute to get list of pets)
#prints the pets info
def view_pets(current_user):
    for pet in current_user.pets:
        pet.display()
#Create pets function
#gets pets info from user
#create Pets() from the info
#print new pet
def create_pet(current_user):
    name = input("Pet name: ")
    species = input("Pet species: ")
    breed = input("Pet breed: ")
    age = input("Pet age: ")

    new_pet = Pets(name=name, species=species, breed=breed, age=age, owner_id=current_user.id)

    session.add(new_pet)
    session.commit()
    print("Pet profile successfully created!")
#Update pets function
#display current users pets
#allow them to select a pet BY NAME
#query that pet from the database
#get updated info from the user
#set that pets info to the new info
#commit changes
#print new pet info
def update_pet(current_user):
    view_pets(current_user)
    choice = input("Enter name of pet to update: ")
    pet = session.query(Pets).where(Pets.name.ilike(choice), Pets.owner_id == current_user.id).first() # Searching for a pet that has the given name and belongs to the user
    if pet:
        print("To keep information leave fields blank.")
        name = input("Pet name: ")
        species = input("Pet species: ")
        breed = input("Pet breed: ")
        age = input("Pet age: ")
        if name:
            pet.name = name
        if species:
            pet.species = species
        if breed:
            pet.breed = breed
        if age:
            pet.age = age       
        session.commit()
        print("------- Updated Pet ------------")
        pet.display()
    else:
        print("Invalid Pet Selection.")



#Delete pets function
#display current users pets
#allow them to select a pet BY NAME
#query that pet from the database
#Ask user if they are sure they want to delete this pet
#delete pet from the session
#commit changes




