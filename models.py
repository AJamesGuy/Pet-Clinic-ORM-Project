from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean, Text, text
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase, Mapped, mapped_column
from datetime import datetime, date

# Database setup
engine = create_engine('sqlite:///pet_clinic.db')
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass


class Owner(Base):
    """Owner model representing pet owners"""
    __tablename__ = 'owners'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Relationship to pets (one-to-many)
    pets: Mapped[list["Pet"]] = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="owner")
    

    def display(self):
        print("----------- My Info ----------")
        print("Name:", self.name)
        print("Email:", self.email)
        print("Phone:", self.phone)
    


class Pet(Base):
    """Pet model representing pets in the clinic"""
    __tablename__ = 'pets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "Dog", "Cat", "Bird"
    breed: Mapped[str] = mapped_column(String(100), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('owners.id'), nullable=False)
    
    # Relationships
    owner: Mapped["Owner"] = relationship("Owner", back_populates="pets")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="pet")
    
    def display(self):
        print("Name: ", self.name)
        print("Species: ", self.species)
        print("Breed: ", self.breed)
        print("Age: ", self.age)



class Vet(Base):
    """Veterinarian model representing clinic veterinarians"""
    __tablename__ = 'vets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100), nullable=True)  # e.g., "General", "Surgery", "Dermatology"
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    def display(self):
        print("ID:", self.id)
        print("Name:", self.name)
        print("Specialization:", self.specialization)
        print("Email:", self.email)
    
    # Relationships
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="vet")
    
    
class Appointment(Base):
    """Appointment model representing pet appointments with veterinarians"""
    __tablename__ = 'appointments'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey('pets.id'), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('owners.id'), nullable=False)
    veterinarian_id: Mapped[int] = mapped_column(ForeignKey('vets.id'), nullable=False)
    appointment_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="Scheduled", nullable=False)  # "Scheduled", "Completed", "Cancelled"
    
    # Relationships
    pet: Mapped["Pet"] = relationship("Pet", back_populates="appointments")
    vet: Mapped["Vet"] = relationship("Vet", back_populates="appointments")
    owner: Mapped["Owner"] = relationship("Owner", back_populates="appointments")

    def display(self):
        print("Appointment ID:", self.id)
        print(f"Pet Name: {self.pet.name if self.pet else 'N/A'}")
        print(f"Vet Name: {self.vet.name if self.vet else 'N/A'}")
        print("Date:", self.appointment_date)
        print("Status:", self.status)
        print("Notes:", self.notes)
    
    
    
    


# Run once to create tables


def seed():
    """Function to seed initial data into the database for testing purposes."""
    print("Creating database and tables...")
    # Uncomment the next line if you want to drop existing tables
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with Session() as session:
        print("Seeding initial data...")
        owner_one = Owner(name="Harry Guliver", phone=1234567890, email="Guliver@gmail.com", password="password123")
        owner_two = Owner(name="Sally Brown", phone=9876543210, email="Sally@Brown.com", password="mypassword")
        owner_three = Owner(name="Tommy Lee", phone=5556667777, email="Tommyboy@yahoo.com", password="tommy1234")
        session.add_all([owner_one, owner_two, owner_three])

        pet_one = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=3, owner_id=1)
        pet_two = Pet(name="Mittens", species="Cat", breed="Siamese", age=2, owner_id=2)
        pet_three = Pet(name="Charlie", species="Dog", breed="Beagle", age=4, owner_id=3)
        pet_four = Pet(name="Luna", species="Cat", breed="Maine Coon", age=1, owner_id=1)
        pet_five = Pet(name="Max", species="Bird", breed="Parakeet", age=5, owner_id=2)
        pet_six = Pet(name="Sharon", species="Bird", breed="Parrot", age=2, owner_id=3)
        session.add_all([pet_one, pet_two, pet_three, pet_four, pet_five, pet_six])
        
        vet1 = Vet(name="Dr. Dizzy", specialization="Dogs, Cats", email="dylank@clinic.com")
        vet2 = Vet(name="Dr. James Brown", specialization="Birds", email="james.brown@clinic.com")
        vet3 = Vet(name="Dr. Lisa Garcia", specialization="Bunny's", email="lisa.garcia@clinic.com")
        vet4 = Vet(name="Dr. Emily Wilson", specialization="General", email="emily.wilson@clinic.com")
        session.add_all([vet1,vet2,vet3,vet4])

        session.commit()
        print("Database seeded successfully.")


if __name__ == "__main__":
    seed()