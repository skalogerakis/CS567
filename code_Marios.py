from owlready2 import *

onto = get_ontology("http://mariostest.org/onto.owl")

# Define basic abstract Concept 
class NaturalSatellite(Thing):
    namespace = onto

class ArtificialSatellite(Thing): #??
    namespace = onto
    is_a = [Not(NaturalSatellite)] # 4) Artificial Satellite is not a natural satellite


class orbitsAround(ObjectProperty):
    namespace = onto
    domain = [Thing] # anything - no constrain
    range = [Thing] # anything - no constrain

class hasMember(ObjectProperty):
    namespace = onto
    domain = [Thing] # anything - no constrain
    range = [Thing] # anything - no constrain

class locatedIn(ObjectProperty):
    namespace = onto
    domain = [Thing] # anything - no constrain
    range = [Thing] # anything - no constrain

# locatedIn.equivalent_to.append([Inverse(hasMember)]) # 1) If you are located somewhere, you are a member of this place. # error

class observes(ObjectProperty):
    namespace = onto
    domain = [Thing] # anything - no constrain
    range = [Thing] # anything - no constrain


class locatedIn(ObjectProperty):
    namespace = onto
    domain = [Thing] # anything - no constrain
    range = [Thing] # anything - no constrain

class hasForSatellite(ObjectProperty):
    namespace = onto
    domain = [Thing] # anything - no constrain
    range = [Thing] # anything - no constrain

class isSatelliteOf(ObjectProperty):
    namespace = onto
    domain = [Thing] # anything - no constrain
    range = [Thing] # anything - no constrain

# isSatelliteOf.is_a.append([orbitsAround.some(Thing)]) #13) If something is a satellite then it orbits # ERROR
# isSatelliteOf.is_a.append([Inverse(hasForSatellite)]) #15) Is satellite of is the inverse of has for Satellite # ERROR


class Star(Thing):
    namespace = onto

class hasCenterOfMass(FunctionalProperty): # 16) hasCenterOfMass is functional
    namespace = onto

class Universe(Thing):
    namespace = onto

class Galaxy(Thing):
    namespace = onto

# ERROR
# Galaxy.is_a.append([locatedIn.some(Universe) & hasMember.some(Star) & hasCenterOfMass.some(Thing)]) # 2) A galaxy is located in the universe and there is some star that is member of this galaxy and galaxy has at most one center of Mass

class Universe(Thing):
    namespace = onto
    is_a = [hasMember.min(1,Galaxy)] #8) Every universe has at least one galaxy

class CelestialBody(Thing):
    namespace = onto
    is_a = [locatedIn.some(Galaxy)] #7) Celestial body is located in a galaxy

class Satellite(Thing):
    namespace = onto
    is_a = [CelestialBody & orbitsAround.some(Thing) ] # 17) A satellite is a celestial body that orbits around something

# ERROR
# Satellite.equivalent_to.append(Or([NaturalSatellite,ArtificialSatellite])) # 18) A satellite is equivalent to a natural satellite or a artificial satellite
# AllDisjoint([ArtificialSatellite, NaturalSatellite]) ## ??
# Satellite.equivalent_to.append(Or([ArtificialSatellite,NaturalSatellite]))  # 18) Satellite is equivalent to Artificial Satellite or Natural Satellite

class DarkMatter(Thing):
    namespace = onto

class NormalMatter():
    namespace = onto
    is_a = [Not(DarkMatter)]  # 5) Normal Matter is not Dark Matter 

class Asteroid(CelestialBody): # 12) Asteroid is a CelestialBody
    namespace = onto

class Comet(CelestialBody): # 11) Comet is a CelestialBody
    namespace = onto

class pullGravity(SymmetricProperty): # 14) If something is pulled by gravity then gravity pull it
    namespace = onto

class SpaceTelescope(Thing):
    namespace = onto
    is_a = [CelestialBody & observes.some(CelestialBody)] # 10) A space telescope is a celestial body that observes other celestial bodies 


class Planet(Thing):
    namespace = onto
    is_a = [CelestialBody & orbitsAround.some(Star)] #6) A planet is a celestial body that orbits around a star

class DwarfPlanet(Thing):
    namespace = onto
    is_a = [CelestialBody & orbitsAround.some(Star) & Not(isSatelliteOf.some(Planet))] # 9) A dwarf planet is a celestial body that orbits around a star and that is not a satellite of a planet


class PlanetSystemBody(Thing):
    namespace = onto
    is_a = [CelestialBody & Not( Or( [Planet,DwarfPlanet,NaturalSatellite]))] # 3_ A planetary system body is a celestial body that is not a planet nor a dwarf planet nor a natural satellite

# Define rules 
    
# print(onto.base_iri)
# print(onto.imported_ontologies)



if __name__ == '__main__':

    ## A-Box

    # Asteroid 
    asteroid1 = Asteroid("Eros")
    asteroid2 = Asteroid("Ikarus")
    asteroid3 = Asteroid("Ceres")
    asteroid4 = Asteroid("Pallas")

    # Comet
    comet1 = Comet("Chiron")
    comet2 = Comet("Borrely")
    comet3 = Comet("Halley")
    comet4 = Comet("Enke")

    # SpaceTelescope
    spaceTelescope1 = SpaceTelescope("Hubble")
    spaceTelescope2 = SpaceTelescope("MOST")
    spaceTelescope3 = SpaceTelescope("EUVE")

    # ArtificialSatellite
    artifSatellite1 = ArtificialSatellite("Sputnik")
    artifSatellite2 = ArtificialSatellite("Glory")

    # NaturalSatellite
    naturSatellite1 = NaturalSatellite("Moon")
    naturSatellite2 = NaturalSatellite("Europa")
    naturSatellite3 = NaturalSatellite("Triton")

    # Dwarf Planet
    drarfPlanet1 = DwarfPlanet("Ceres")
    drarfPlanet2 = DwarfPlanet("Pluto")
    drarfPlanet3 = DwarfPlanet("Makemake")
    drarfPlanet4 = DwarfPlanet("Eris")

    # Star
    star1 = Star("Sun")
    star2 = Star("Sirius")
    star3 = Star("Rigel")
    star4 = Star("Pleiades")

    # Planet
    planet1 = Planet("Earth")
    planet2 = Planet("Mars")
    planet3 = Planet("Jupiter")
    planet4 = Planet("Venus")
    planet5 = Planet("Saturn")

    # PlanetSystemBody
    planetSysBody1 = PlanetSystemBody("Enke")
    planetSysBody2 = PlanetSystemBody("Haleys")
    planetSysBody3 = PlanetSystemBody("Ceres")
    planetSysBody4 = PlanetSystemBody("Icarus")

    # CelestialBody
    celectialBody1 = CelestialBody("Moon")
    celectialBody2 = CelestialBody("Sun")
    celectialBody3 = CelestialBody("Mars")
    celectialBody4 = CelestialBody("Pluto")

    # Galaxy
    galaxy1 = Galaxy("Milkyway")
    galaxy2 = Galaxy("Andromeda")
    galaxy3 = Galaxy("Cyganus")



    # Rules instances
    
    # ERROR BELOW..........
    # orbitsAround
    # orbitsAround1 = orbitsAround("Hubble","Earth")
    # orbitsAround2 = orbitsAround("Moon","Earth")
    # orbitsAround3 = orbitsAround("Earth","Sun")
    # orbitsAround4 = orbitsAround("Mars","Sun")

    # # locatedIn
    # locatedIn1 = locatedIn("Planet", "Galaxy")

    # # hasMember
    # hasMember1 = hasMember("Galaxy" , "Planet")
    # hasMember2 = hasMember("Galaxy" , "Dwarf")
    # hasMember3 = hasMember("Galaxy" , "Comet") #  like     hasMember3 = hasMember("Milkyway" , "Chiron")
    # hasMember4 = hasMember("Galaxy" , "Asteroid") ############# here instances not ???

    # ...

    onto.save(file = "onto_marios.owl", format = "rdfxml")

print("ok")