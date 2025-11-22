from models import Pet, session

#view pets function
#Takes in current user
#Loops over all of the current users pets (use the .pets relationship attribute to get list of pets)
#prints the pets info
def view_pets(current_user):
    if not current_user.pets:
        print("You have no pets registered.")
        return
    for pet in current_user.pets:
        pet.display()
        print("\n---------------------\n")
#Create pets function
#gets pets info from user
#create Pets() from the info
#print new pet
def create_pet(current_user):
    name = input("Pet name: ").strip()
    species = input("Pet species: ").strip()
    breed = input("Pet breed: ").strip()
    age = input("Pet age: ").strip()

    new_pet = Pet(name=name, species=species, breed=breed, age=age, owner_id=current_user.id)

    session.add(new_pet)
    session.commit()
    print("Pet profile successfully created!")
    new_pet.display()
#Update pets function
#display current users pets
#allow them to select a pet BY NAME
#query that pet from the database
#get updated info from the user
#set that pets info to the new info
#commit changes
#print new pet info
def update_pet(current_user):
    if not current_user.pets:
        print("You have no pets to update.")
        return
    view_pets(current_user)
    choice = input("Enter name of pet to update: ").strip()
    pet = session.query(Pet).where(Pet.name.ilike(choice), Pet.owner_id == current_user.id).first() # Searching for a pet that has the given name and belongs to the user
    if not pet:
        print("Pet not found or doesn't belong to you.")
        return
    
    if pet:
        print("To keep information leave fields blank.")
        name = input(f"New name: (current: {pet.name}): ").strip()
        species = input(f"New species (current: {pet.species}): ").strip()
        breed = input(f"New breed (current: {pet.breed}): ").strip()
        age = input(f"New age (current: {pet.age}): ").strip()

        if name:
            pet.name = name
        if species:
            pet.species = species
        if breed:
            pet.breed = breed
        if age:
            try:
                pet.age = int(age)
            except ValueError:
                print("Invalid age input. Age not updated.")

        session.commit()
        print("------- Updated Pet ------------")
        pet.display()


#Delete pets function
#display current users pets
#allow them to select a pet BY NAME
#query that pet from the database
#Ask user if they are sure they want to delete this pet
#delete pet from the session
#commit changes

def delete_pet(current_user):
    if not current_user.pets:
        print("You have no pets to delete.")
        return
    
    view_pets(current_user)
    choice = input("Enter the name of the pet to delete: ").strip()
    pet = session.query(Pet).where(Pet.name.ilike(choice), Pet.owner_id == current_user.id).first()
    if not pet:
        print("Pet not found or doesn't belong to you.")
        return
    print(f"\nAre you sure you want to delete {pet.name}? This action cannot be undone.")
    confirm = input("Type 'DELETE' to confirm: ").strip()
    if confirm == "DELETE":
        session.delete(pet)
        session.commit()
        print(f"{pet.name} has been deleted.")
    else:
        print("Pet deletion cancelled.")
    


