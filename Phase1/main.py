from owlready2 import *

onto = get_ontology("http://skalogerakis.org/onto.owl")


############################ ROLES #######################################

class hasMember(ObjectProperty):
    namespace = onto


class locatedIn(ObjectProperty):
    namespace = onto
    inverse_property = hasMember  # 1) locatedIn is equivalent to the Inverse of hasMember

    '''
        NOTE: In the definition of our Tbox using DL, these two rules are considered equivalent. 
        The reason behind that choice was to present the DL rules as closely to the Python API
        as possible. The documentation states that two properties are inverse if they express the
        same meaning but in a reversed way. The API also automatically handles inverse relations 
        and automatically updates the corresponding relation. So it is considered as a bidirectional property
        and we define it as one
    '''


class pullGravity(ObjectProperty, SymmetricProperty):  # 14) Something that is pulled by gravity then gravity pulls it
    namespace = onto


'''
    NOTE: Chose to add directly FunctionalProperty here. Could also use the role with cardinality
    .max(1) to infer that this role is functional as the documentation states but chose this way
'''


class hasCenterOfMass(ObjectProperty, FunctionalProperty):  # 16) hasCenterOfMass is Functional
    namespace = onto


class orbitsAround(ObjectProperty):
    namespace = onto


class observes(ObjectProperty):
    namespace = onto


class isSatelliteOf(
    orbitsAround):  # 13) If something is satellite then it orbits (isSatelliteOf is subproperty of orbitsAround)
    namespace = onto


class hasForSatellite(ObjectProperty):
    namespace = onto
    inverse_property = isSatelliteOf  # 15) isSatelliteOf is equivalent to hasForSatellite. The same comments that are below locatedIn class are applied here


############################ CONCEPTS #####################################


class Universe(Thing):
    namespace = onto


class Star(Thing):
    namespace = onto


class Galaxy(Thing):
    namespace = onto
    is_a = [locatedIn.some(Universe) & hasMember.some(Star) & hasCenterOfMass.some(Thing)]  # 2) A galaxy is located in the universe and there is some star
                                                                                            # that is a member of this galaxy and galaxy and hasCenterOfMass
                                                                                            # TODO if defined without some, then creates a new class in Protege


Universe.is_a.append(hasMember.min(1, Galaxy))  # 8) Every Universe has at least one galaxy. Must define it here since we have not Galaxy when defining Universe class


class CelestialBody(Thing):
    namespace = onto
    is_a = [locatedIn.some(Galaxy)]  # 7) A celestial body is located in a galaxy


class Planet(Thing):
    namespace = onto
    is_a = [CelestialBody & orbitsAround.some(Star)]  # 6) A planet is a celestial body that orbits around a Star


class DwarfPlanet(Planet):
    namespace = onto
    is_a = [Planet & Not(isSatelliteOf.some(
        Planet))]  # 9) Dwarf planet is a planet that is not a satellite of a planet TODO Swithced the original defintion


class Satellite(Thing):
    namespace = onto
    is_a = [
        CelestialBody & orbitsAround.some(Thing)]  # 17) A satellite is a celestial body that orbits around something.
    # That is the way that Top concept is defined here, otherwise we get an error


class NaturalSatellite(Satellite):
    namespace = onto


class ArtificialSatellite(Satellite):
    namespace = onto
    is_a = [Not(NaturalSatellite)]  # 4) Artificial Satellite is not a natural satellite.


NaturalSatellite.is_a.append(Not(ArtificialSatellite))  # 19) Natural Satellite in not an artificial satellite

'''
    This is the key for rule 18)
    In ontologies an individual can belong to several classes. Therefore, a
    given satellite can very well be both Natural and Artificial.(Open World Assumption)
    For that reason, declare classes as disjoint. These cannot have individuals in common!!
    So the result will be either Natural or Artificial Satellite
'''
AllDisjoint([ArtificialSatellite, NaturalSatellite])
Satellite.equivalent_to.append(Or([ArtificialSatellite,
                                   NaturalSatellite]))  # 18) Satellite is equivalent to Artificial Satellite or Natural Satellite


class NormalMatter(Thing):
    namespace = onto


class DarkMatter(Thing):
    namespace = onto
    is_a = [Not(NormalMatter)]  # 20) DarkMatter is not Normal Matter


AllDisjoint([NormalMatter, DarkMatter])  # Normal and DarkMatter must be disjoint
NormalMatter.is_a.append(Not(DarkMatter))  # 5) NormalMatter is not Dark Matter


class SpaceTelescope(Thing):
    namespace = onto
    is_a = [CelestialBody & observes.some(
        CelestialBody)]  # 10) A space telescope is a celestial body that observes some celestial body


class Comet(CelestialBody):  # 11) Comet is a celestial body (is a subclass of)
    namespace = onto


class Asteroid(CelestialBody):  # 12) Asteroid is a celestial body (is a subclass of)
    namespace = onto


class PlanetarySystemBody(Thing):
    namespace = onto
    is_a = [CelestialBody & Not(Planet) & Not(DwarfPlanet) & Not(
        NaturalSatellite)]  # 3) A planetary system Body is a celestial body
    # that is not a planet nor a dwarf planet not a satellite


if __name__ == '__main__':
    # print(locatedIn.domain)

    # print('Satellite subclasses ', [x for x in Satellite.subclasses()])
    #
    # print("Is a ART ", ArtificialSatellite.is_a)
    # print("Is a NAT ", NaturalSatellite.is_a)
    # print("Desc ", NaturalSatellite.descendants())
    # print("Ans ", ArtificialSatellite.ancestors())

    ############################ ABOX #####################################

    # Galaxy Concepts
    Milkyway = Galaxy("Milkyway")
    Andromeda = Galaxy("Andromeda")
    Cygunus = Galaxy("Cygunus")

    # Celestial Body Concepts
    Moon = CelestialBody("Moon")
    Sun = CelestialBody("Sun")
    Mars = CelestialBody("Mars")
    Pluto = CelestialBody("Pluto")

    # Planetary System Body
    Enke = PlanetarySystemBody("Enke")
    Halley = PlanetarySystemBody("Halley") # mini change from "haleys" to Halley
    Ceres = PlanetarySystemBody("Ceres")
    Icarus = PlanetarySystemBody("Icarus")

    # Planet
    Earth = Planet("Earth")
    Mars = Planet("Mars")
    Jupiter = Planet("Jupiter")
    Venus = Planet("Venus")
    Saturn = Planet("Saturn")

    # Star
    Sun = Star("Sun")
    Sirius = Star("Sirius")
    Rigel = Star("Rigel")
    Pleiades = Star("Pleiades")

    # Dwarf Planet
    Ceres = DwarfPlanet("Ceres")
    Pluto = DwarfPlanet("Pluto")
    Makemake = DwarfPlanet("Makemake")
    Eris = DwarfPlanet("Eris")

    # Asteroid
    Eros = Asteroid("Eros")
    Ceres = Asteroid("Ceres")
    Icarus = Asteroid("Icarus")
    Pallas = Asteroid("Pallas")

    # Natural Satellite
    Moon = NaturalSatellite("Moon")
    Europa = NaturalSatellite("Europa")
    Triton = NaturalSatellite("Triton")

    # Artificial Satellite
    Sputnik = ArtificialSatellite("Sputnik")
    Glory = ArtificialSatellite("Glory")

    # Space Telescope
    Hubble = SpaceTelescope("Hubble")
    MOST = SpaceTelescope("MOST")
    EUVE = SpaceTelescope("EUVE")

    # Comet
    Chiron = Comet("Chiron")
    Borrelly = Comet("Borrelly")
    Halley = Comet("Halley")
    Enke = Comet("Enke")
    
    # Normal Matter
    MilkywayNM = NormalMatter("MilkywayNM")
    
    # Dark Matter
    MilkywayDM = DarkMatter("MilkywayDM")
    
    # Combination with roles
    # orbitsAround
    Moon.orbitsAround = [Earth]    # Moon orbitsAround Earth
    Hubble.orbitsAround = [Earth]
    Sputnik.orbitsAround = [Earth]
    Earth.orbitsAround = [Sun]
    Mars.orbitsAround = [Sun] 

    # hasMember - locatedIn
    Milkyway.hasMember = [Sun, Sirius, Rigel, Earth, Mars , Pallas,Icarus,Ceres] 


    # hasForSatellite - isSatelliteOf
    Earth.hasForSatellite = [Moon,Glory,Sputnik]

    # observes
    Hubble.observes = [Earth]
    MOST.observes = [Earth]
    EUVE.observes = [Milkyway]

    # pullGravity
    Earth.pullGravity = [Moon,Sun,Hubble,Sputnik]
    Sun.pullGravity = [Earth,Jupiter,Venus,Saturn,Icarus]
    
    MilkywayNM.pullGravity=[MilkywayDM]

    # hasCenterOfMass
    Cygunus.hasCenterOfMass = Thing
    Andromeda.hasCenterOfMass = Thing
    Milkyway.hasCenterOfMass = Thing

    onto.save(file="main_final_onto.owl", format="rdfxml")
