from datetime import datetime
import os
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name, species):
        self._name = name
        self._species = species
        self._last_fed = None
    
    @property
    def name(self):
        return self._name
    
    @property
    def species(self):
        return self._species
    
    @property
    def last_fed(self):
        return self._last_fed
    
    @abstractmethod
    def make_sound(self):
        pass
    
    @abstractmethod
    def feed(self):
        pass
    
    def __str__(self):
        return f"{self._name} the {self._species}"

class Lion(Animal):
    def __init__(self, name):
        super().__init__(name, "Lion")
    
    def make_sound(self):
        return "ROAR!"
    
    def feed(self):
        self._last_fed = datetime.now()
        return f"{self._name} was fed meat at {self._last_fed.strftime('%H:%M')}"

class Penguin(Animal):
    def __init__(self, name):
        super().__init__(name, "Penguin")
    
    def make_sound(self):
        return "Honk honk!"
    
    def feed(self):
        self._last_fed = datetime.now()
        return f"{self._name} was fed fish at {self._last_fed.strftime('%H:%M')}"

class Monkey(Animal):
    def __init__(self, name):
        super().__init__(name, "Monkey")
    
    def make_sound(self):
        return "Ooh ooh ah ah!"
    
    def feed(self):
        self._last_fed = datetime.now()
        return f"{self._name} was fed bananas at {self._last_fed.strftime('%H:%M')}"

class ZooKeeper:
    def __init__(self, name):
        self._name = name
        self._assigned_animals = []
    
    @property
    def name(self):
        return self._name
    
    def assign_animal(self, animal):
        self._assigned_animals.append(animal)
        return f"{animal.name} assigned to {self._name}"
    
    def feed_animals(self):
        return [animal.feed() for animal in self._assigned_animals]

class Zoo:
    _instance = None
    
    def __new__(cls, name):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._name = name
            cls._instance._animals = []
            cls._instance._zookeepers = []
            cls._instance._opening_time = "9:00 AM"
            cls._instance._closing_time = "6:00 PM"
        return cls._instance
    
    @property
    def name(self):
        return self._name
    
    def add_animal(self, animal):
        self._animals.append(animal)
        return f"Added {animal.name} to {self._name}"
    
    def add_zookeeper(self, zookeeper):
        self._zookeepers.append(zookeeper)
        return f"Added zookeeper {zookeeper.name}"
    
    def daily_routine(self):
        print(f"\n=== {self._name} Daily Routine ===")
        print(f"Opening Hours: {self._opening_time} to {self._closing_time}")
        
        print("\nFeeding Time:")
        for keeper in self._zookeepers:
            print(f"{keeper.name} is feeding:")
            for result in keeper.feed_animals():
                print(f"- {result}")
        
        print("\nAnimal Sounds:")
        for animal in self._animals:
            print(f"{animal.name} says: {animal.make_sound()}")
    
    def save_to_file(self, filename="zoo_data.txt"):
        with open(filename, 'w') as f:
            f.write(f"ZOO:{self._name}\n")
            for animal in self._animals:
                f.write(f"ANIMAL:{animal.__class__.__name__},{animal.name}\n")
            for keeper in self._zookeepers:
                f.write(f"KEEPER:{keeper.name}\n")
                for animal in keeper._assigned_animals:
                    f.write(f"ASSIGNMENT:{keeper.name},{animal.name}\n")
        print(f"Saved zoo data to {filename}")
    
    def load_from_file(self, filename="zoo_data.txt"):
        if not os.path.exists(filename):
            print("No save file found. Starting fresh zoo.")
            return
        
        self._animals = []
        self._zookeepers = []
        
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line.startswith("ZOO:"):
                self._name = line.split(":")[1]
            elif line.startswith("ANIMAL:"):
                parts = line.split(":")[1].split(",")
                animal_class = parts[0]
                animal_name = parts[1]
                
                if animal_class == "Lion":
                    animal = Lion(animal_name)
                elif animal_class == "Penguin":
                    animal = Penguin(animal_name)
                elif animal_class == "Monkey":
                    animal = Monkey(animal_name)
                
                self.add_animal(animal)
            elif line.startswith("KEEPER:"):
                keeper_name = line.split(":")[1]
                self.add_zookeeper(ZooKeeper(keeper_name))
            elif line.startswith("ASSIGNMENT:"):
                parts = line.split(":")[1].split(",")
                keeper_name = parts[0]
                animal_name = parts[1]
                
                keeper = next((k for k in self._zookeepers if k.name == keeper_name), None)
                animal = next((a for a in self._animals if a.name == animal_name), None)
                
                if keeper and animal:
                    keeper.assign_animal(animal)

    def show_all_animals(self):
        if not self._animals:
            print("\nNo animals in the zoo yet!")
            return
            
        print("\n=== All Animals in Zoo ===")
        for i, animal in enumerate(self._animals, 1):
            last_fed = f"Last fed: {animal.last_fed.strftime('%Y-%m-%d %H:%M')}" if animal.last_fed else "Not fed yet"
            print(f"{i}. {animal.name} ({animal.species}) - {last_fed}")

    def set_name(self, new_name):
        self._name = new_name

def main():
    print("Welcome to Zoo Management System!")
    
    zoo = Zoo("Temporary Name")
    zoo.load_from_file()
    
    if not zoo.name or (not zoo._animals and not zoo._zookeepers):
        zoo_name = input("Enter zoo name: ")
        zoo.set_name(zoo_name)
    
    while True:
        print("\nMenu:")
        print("1. Add Animal")
        print("2. Add ZooKeeper")
        print("3. Assign Animal to ZooKeeper")
        print("4. Run Daily Routine")
        print("5. Save Zoo Data")
        print("6. Show All Animals")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            print("\nAnimal Types:")
            print("1. Lion")
            print("2. Penguin")
            print("3. Monkey")
            
            animal_type = input("Select animal type (1-3): ")
            name = input("Enter animal name: ")
            
            if animal_type == "1":
                animal = Lion(name)
            elif animal_type == "2":
                animal = Penguin(name)
            elif animal_type == "3":
                animal = Monkey(name)
            else:
                print("Invalid choice")
                continue
            
            print(zoo.add_animal(animal))
        
        elif choice == "2":
            name = input("Enter zookeeper name: ")
            keeper = ZooKeeper(name)
            print(zoo.add_zookeeper(keeper))
        
        elif choice == "3":
            if not zoo._zookeepers or not zoo._animals:
                print("You need both animals and zookeepers first!")
                continue
            
            print("\nAvailable Zookeepers:")
            for i, keeper in enumerate(zoo._zookeepers, 1):
                print(f"{i}. {keeper.name}")
            
            keeper_idx = int(input("Select zookeeper (number): ")) - 1
            
            print("\nAvailable Animals:")
            for i, animal in enumerate(zoo._animals, 1):
                print(f"{i}. {animal.name} ({animal.species})")
            
            animal_idx = int(input("Select animal (number): ")) - 1
            
            try:
                keeper = zoo._zookeepers[keeper_idx]
                animal = zoo._animals[animal_idx]
                print(keeper.assign_animal(animal))
            except IndexError:
                print("Invalid selection")
        
        elif choice == "4":
            zoo.daily_routine()
        
        elif choice == "5":
            zoo.save_to_file()
            print("Zoo data saved!")
        
        elif choice == "6":
            zoo.show_all_animals()
        
        elif choice == "7":
            save = input("Save before exiting? (y/n): ").lower()
            if save == "y":
                zoo.save_to_file()
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()