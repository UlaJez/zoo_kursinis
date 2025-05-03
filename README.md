# Zoo management

Mano sukurta programa yra skirta virtualaus zoologijos sodo valdymui, naudojant objektinio programavimo principus.

# Kaip naudotis programa
1. Paleisti programą.

2. Susikurti norimus gyvūnus, zoologijos sodo prižiūrėtojus, priskirti prižiūrėtojams gyvunus ir t.t.

3. Išsaugoti duomenis.

4. Išeiti.

Zoologijos sodo duomenys bus išsaugoti faile "zoo_data.txt", o vėliau iš šio failo bus skaitomi duomenys ir bus galima tęsti zoologijos sodo papildymą.

### Reikalavimai:
+ Polymorphism
+ Abstraction
+ Inheritance
+ Encapsulation

# Polimorfizmas
Polimorfizmas reiškia, kad skirtingos klasės gali naudoti tą patį metodą, bet kiekviena jį įgyvendina savo būdu.

Mano kode polimorfizmą galime pastebėti šiose vietose:
```python
class Lion(Animal):
    def make_sound(self):
        return "ROAR!"

class Penguin(Animal):
    def make_sound(self):
        return "Honk honk!"

class Monkey(Animal):
    def make_sound(self):
        return "Ooh ooh ah ah!"
```
Kreipiantis į metodą make_sound, grąžinami skirtingi gyvunų garsai.

# Abstrakcija

Mano kode abstrakciją galime pastebėti šioje vietoje:
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def feed(self):
        pass

class Lion(Animal):
    def make_sound(self):
        return "ROAR!"
    
    def feed(self):
        self._last_fed = datetime.now()
        return f"{self._name} was fed meat at {self._last_fed.strftime('%H:%M')}"
```
Metodai make_sound ir feed yra privalomi.

# Paveldėjimas
Paveldėjimas leidžia kurti naujas klases, kurios perima savybes ir metodus iš esamų klasių.

Mano projekte yra paveldima klasė Animal ir ją paveldi kiti gyvūnai (Lion, Penguin ir Monkey):
```python
class Animal(ABC):
    def __init__(self, name, species):
        self._name = name
        self._species = species
        self._last_fed = None

class Lion(Animal):
    def __init__(self, name):
        super().__init__(name, "Lion")

class Penguin(Animal):
    def __init__(self, name):
        super().__init__(name, "Penguin")

class Monkey(Animal):
    def __init__(self, name):
        super().__init__(name, "Monkey")
```

# Inkapsuliacija
Inkapsuliacija – objektinio programavimo principas, pagal kurį objekto vidiniai duomenys yra slepiami ir jais galima manipuliuoti tik naudojant objekto viešus metodus.

Mano projekte yra naudojami protected atributai:
```python
class Animal(ABC):
    def __init__(self, name, species):
        self._name = name
        self._species = species

@property
    def name(self):
        return self._name
    
    @property
    def species(self):
        return self._species
```
### Design pattern'as
Savo kode naudojau Singleton design pattern'ą. Jis užtikrina, kad (šiuo atveju) sukurtas zoologijos sodas yra tik vienas.

Mano projekte Singleton naudojamas Zoo klasėje:
```pyton
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
```

# Kompozicija ir agregacija
Kompozicija - tai stipri "yra sudarytas iš" ryšio forma tarp objektų. Vienas objektas visiškai priklauso kitam ir negali egzistuoti be jo.

Agregacija - tai silpnesnis "turi" ryšys. Objektai yra susiję, bet gali egzistuoti atskirai. Savo projekte naudoju agregaciją:
```python
class ZooKeeper:
    def __init__(self, name):
        self._name = name
        self._assigned_animals = []

 def assign_animal(self, animal):
        self._assigned_animals.append(animal)
        return f"{animal.name} assigned to {self._name}"
```
Zookeeper turi sarašą Animal objektų, bet jų pats nesukuria. Taip pat gyvunai gali priklausyti ir be zoologijos sodo prižiūrėtojo. Jei ištrinsime Zookeeper, gyvūnai išlieka.

# Reading from file & writing to file

Mano projekte yra skaitoma bei įrašoma į tekstinį failą "zoo_data.txt". Jei anksčiau nėra sukurtas toks tekstinis failas, jis yra sukuriamas naujas, kai paleidžiame kodą. Per konsolę galime pridėti gyvunus, zookeeper'ius, priskirti prižiūrėtojams gyvunus, tuomet tie prižiūrėtojai gali juos pamaotinti. Sukurti nauji prižiūrėtojai, gyvūnai bei gyvūno priskyrimas prižiūrėtojui yra išsaugomi "zoo_data.txt" faile. Vėliau paleidus šią programą vėl, bus įkeliami visi duomenys.

Rašymas:
```python
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
```
Skaitymas:
```python
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
```
# Rezultatai:
+ Programa sėkmingai kuria zoologijos sodo sistemą su gyvūnais bei jų prižiūrėtojais.
+ Sistema išsaugo zoo duomenis aiškiu, eilutėmis paremtu formatu (pvz., ZOO:, ANIMAL:), kas palengvina duomenų analizę ir objektų atkūrimą paleidimo metu.
+ Kol kas sistema nenumato blogai suformuotų duomenų apdorojimo, todėl gali kilti klaidų, jei duomenys neatitinka numatyto formato.
+ Vienas iš išūkių buvo tinkamai naudoti skaitymą bei rašymą į failus, kadangi to dar nebuvo tekę daryti.

# Išvados
+ Sukurta funkcionali zoo valdymo sistema, kuri leidžia kaupti gyvūnų ir prižiūrėtojų duomenis, valdyti gyvūnų prižiūrėjimą, skaityti bei rašyti į failą.
+ Veikia Singleton šablonas, įgyvendinta agregacija (laisvi ryšiai tarp objektų), galima papildyti sistemą naujais gyvūnų tipais.
+ Ateityje galima pridėti daugiau funkcionalumų (pvz.: pridėti enclosures, veterinarus), taip pat pasinaudojus Observer design pattern'ą būtų galima padaryti automatinius pranešimus apie gyvūnų savijautą ir t.t.
