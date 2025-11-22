from models import Owner, Pet, Vet, session, Appointment
from datetime import datetime, date

#IMPORTANT when creating an appointment, it is required to convert the date string
# "YYYY-MM-DD" int a python date object

date_format = "%Y-%m-%d" #This will be used to format your date

#Syntax for date conversion

# new_date = datetime.strptime("Date String", date_format)
#example


#Create new appointment
#display pets
#Choose the pet you wish to create an appointment for
#query them out of the db using their name
#display vets
#Choose the vet you with to create an appointment with
#Query them out of the db
#Gather the rest of the info for the appointment
#Convert the date string to python date object
#Create the Appointment() (remind you'll need the pet id and the vet id)
def create_appointment(current_user):
  if not current_user.pets:
    print("You need to have a pet to create an appointment.")
    return

  print("Who is this appointment for?")
  for pet in current_user.pets:
    pet.display()
    print("\n---------------------\n")
  
  choice = input("Enter Pet name: ").strip()

  pet = session.query(Pet).where(Pet.name.ilike(choice), Pet.owner_id==current_user.id).first()

  if not pet:
    print("Invalid Pet Option")
    return

  if pet:
    print(f"\nWho should {pet.name} see?")
    all_vets = session.query(Vet).all()
    for vet in all_vets:
      print('-----------------------------')
      vet.display()

    vet_name = input("Enter Vet name (or ID): ").strip()
    if vet_name == "":
      print("Vet selection cannot be blank.")
      return
    vet = None
    if vet_name.isdigit():
      vet = session.get(Vet, int(vet_name)) #if ID is entered, create vet object by querying by ID
    if not vet:
      vet = session.query(Vet).where(Vet.name.ilike(vet_name)).first() # if vet is still None, try querying by name
    if not vet:
      print("Invalid Vet Option") # if vet is still None, print invalid option
      return

    if vet:
      date_str = input(f"When would you like {pet.name} to see {vet.name} (YYYY-MM-DD): ").strip()
      today = date.today()
      if date_str < today.strftime(date_format):
        print("You cannot schedule an appointment in the past.")
        return
      try:
        appointment_date = datetime.strptime(date_str, date_format) #converting date string to datetime object to be stored in db
      except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
      notes = input(f"What's going on with {pet.name}? ").strip()

      new_apt = Appointment(pet_id=pet.id, veterinarian_id=vet.id, owner=current_user, appointment_date=appointment_date, notes=notes)
      session.add(new_apt)
      session.commit()
      print(f"\nSUCCESS! {pet.name} is booked with {vet.name} on {date_str}!")
      return

# view appointments
def view_appointments(current_user):
  if not current_user.appointments:
    print("You have no appointments scheduled.")
    return
  print("Upcoming Appointments:")
  for pet in current_user.pets:
    for appointment in pet.appointments:
      if appointment.status != 'Complete':
        print("-----------------------")
        appointment.display()
  print("\n")
  print("Completed Appointments:")
  for pet in current_user.pets:
    for appointment in pet.appointments:
      if appointment.status == 'Complete':
        print("-----------------------")
        appointment.display()


#Reschedule appointments
#Show appointments with ids (Loop over current user pets, loop over each pets appointments e.g nested loop)
#Select an appointment by id
#ask user for new date
#convert date
#update the appointment date
def reschedule_appointment(current_user):
  if not current_user.appointments:
    print("You have no appointments to reschedule.")
    return
  view_appointments(current_user)
  apt_id = input("Enter appointment ID to reschedule: ").strip()
  if not apt_id.isdigit():
    print("Invalid selection")
    return
  appointment = session.get(Appointment, int(apt_id))
  if appointment.status == 'Complete':
    print("You cannot reschedule a completed appointment.")
    return
  if appointment and appointment.pet.owner_id == current_user.id:
    new_date = input("Enter new date: (YYYY-MM-DD)")
    today = date.today()
    if new_date < today.strftime(date_format):
      print("You cannot schedule an appointment in the past.")
      return
    try:
      new_date = datetime.strptime(new_date, date_format)
    except ValueError:
      print("Invalid date format. Please use YYYY-MM-DD.")
      return
    
    appointment.appointment_date = new_date
    session.commit()
    print(f"Rescheduled appointment for {new_date}")
  else:
    print("Invalid Selection.")

#Complete appointments
#Show appointments with ids (Loop over current user pets, loop over each pets appointments e.g nested loop)
#query the appointment by id
#change appointment.status to 'complete"
#print success message
def complete_appointment(current_user):
  if not current_user.appointments:
    print("You have no appointments to complete.")
    return
  view_appointments(current_user)
  apt_id = input("Enter appointment ID to mark as complete: ")
  if apt_id not in [str(apt.id) for pet in current_user.pets for apt in pet.appointments]:
    print("Invalid selection.")
    return
  appointment = session.get(Appointment, int(apt_id))
  if appointment.status == 'Complete':
    print("This appointment is already marked as complete.")
    return
  if appointment and appointment.pet.owner_id == current_user.id:
    appointment.status = 'Complete'
    session.commit()
    print("Successfully completed appointment!")
    print("-----------------------")
    appointment.display()