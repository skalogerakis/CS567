from owlready2 import *
import subprocess

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
    is_a = [locatedIn.some(Universe) & hasMember.some(Star) & hasCenterOfMass.some(
        Thing)]  # 2) A galaxy is located in the universe and there is some star
    # that is a member of this galaxy and galaxy and hasCenterOfMass
    # TODO if defined without some, then creates a new class in Protege


Universe.is_a.append(hasMember.min(1,
                                   Galaxy))  # 8) Every Universe has at least one galaxy. Must define it here since we have not Galaxy when defining Universe class


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


# Comment out rule 19. TODO change that in the report as well
# NaturalSatellite.is_a.append(Not(ArtificialSatellite))  # 19) Natural Satellite in not an artificial satellite

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


# Comment out rule 5. TODO change that in the report as well
# NormalMatter.is_a.append(Not(DarkMatter))  # 5) NormalMatter is not Dark Matter


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
    # TODO update on the report
    # 3) UPDATED: A planetary system Body is a celestial body that is not a planet not a satellite
    is_a = [CelestialBody & Not(Planet) & Not(NaturalSatellite)]


###############     PHASE 2 METHODS        ######################
def is_consistent(ontology, flag):
    print(list(ontology.inconsistent_classes()))  # TODO remove, for debugging purposes
    if list(ontology.inconsistent_classes()) != [] or flag:
        return "No"
    return "Yes"


def is_of_types(individual):
    types = onto.get_parents_of(individual)
    return types


def get_all_concept_instances(concept):
    return onto.get_instances_of(concept)  # or concept.instances()


def get_all_role_instances(role):  # ?? what is it suppose to print, ta roles mas einai ola object properties
    return onto.get_instances_of(role)  # or role.instances()


def is_subclass_of(C, D):
    subclasses = onto.get_children_of(D)
    if C in subclasses:
        return True
    return False


def get_Smodule(jar_location, method, input_location, term_location, output_location):
    subprocess.call(['java', '-jar', '{}'.format(jar_location),
                     'extract', '--method', '{}'.format(method),
                     '--input', '{}'.format(input_location),
                     '--term-file', '{}'.format(term_location),
                     '--output', '{}'.format(output_location)])


if __name__ == '__main__':
    # print("IRI", ArtificialSatellite.iri)
    ############################ ABOX #####################################

    # Galaxy Concepts
    Milkyway = Galaxy("Milkyway")
    Andromeda = Galaxy("Andromeda")
    Cygunus = Galaxy("Cygunus")

    # Celestial Body Concepts
    # Moon = CelestialBody("Moon")  #UPDATED: Commented out. Defined and later so redundant
    Sun = CelestialBody("Sun")
    # Mars = CelestialBody("Mars")  #UPDATED: Commented out. Defined and later so redundant
    # Pluto = CelestialBody("Pluto")    #UPDATED: Commented out. Defined and later so redundant

    # Planetary System Body
    Enke = PlanetarySystemBody("Enke")
    Halley = PlanetarySystemBody("Halley")
    # Ceres = PlanetarySystemBody("Ceres")  # UPDATED. Comment that out, so that out ontology is consistent
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
    Moon.orbitsAround = [Earth]  # Moon orbitsAround Earth
    Hubble.orbitsAround = [Earth]
    Sputnik.orbitsAround = [Earth]
    Earth.orbitsAround = [Sun]
    Mars.orbitsAround = [Sun]

    # hasMember - locatedIn
    Milkyway.hasMember = [Sun, Sirius, Rigel, Earth, Mars, Pallas, Icarus, Ceres]

    # hasForSatellite - isSatelliteOf
    Earth.hasForSatellite = [Moon, Glory, Sputnik]

    # observes
    Hubble.observes = [Earth]
    MOST.observes = [Earth]
    EUVE.observes = [Milkyway]

    # pullGravity
    Earth.pullGravity = [Moon, Sun, Hubble, Sputnik]
    Sun.pullGravity = [Earth, Jupiter, Venus, Saturn, Icarus]

    MilkywayNM.pullGravity = [MilkywayDM]

    onto.save(file="main_final_onto.owl", format="rdfxml")

    #  PHASE 2 implementation

    print("###### Stage 2 #########")
    
    exception_flag = False  # Flag for OwlReadyInconsistentOntologyError

    try:
        # Todo infer_property_values = True??
        sync_reasoner()
    except OwlReadyInconsistentOntologyError:
        exception_flag = True
    finally:
        print("\n\n###### Stage 2.1 #########")  # Todo ask how to make that inconsistent
        print("Is_consistent?\t ", is_consistent(ontology=onto, flag=exception_flag))

    print("\n\n###### Stage 2.2 #########")
    print(is_of_types(Halley))
    print(is_of_types(Milkyway))
    print(is_of_types(Moon))
    print(is_of_types(Sun))
    print(is_of_types(Earth))   # TODO should it return also that Earth is a celestial body?

    print("\n\n###### Stage 2.3 #########") # TODO you can call an external reasoner, or implement a method of your own
    print(get_all_concept_instances(SpaceTelescope))
    print(get_all_concept_instances(Planet))
    print(get_all_concept_instances(DwarfPlanet))

    # TODO must definitely check that
    print("\n\n###### Stage 2.4 #########")
    print(get_all_role_instances(pullGravity))

    # EUVE.observes = [Milkyway]
    # print(get_all_role_instances(pullGravity))
    # print(onto.observes.getProperties())
    # tst = observes

    # TODO using tableau from a reasoner, e.g., HermiT ???
    print("\n\n###### Stage 2.5 #########")
    print(is_subclass_of(Planet, Galaxy))
    print(is_subclass_of(NaturalSatellite, Satellite))
    print(is_subclass_of(Planet, CelestialBody))    #TODO this is wrong should be True
    print(is_subclass_of(DwarfPlanet, Planet))


    print("\n\n###### BONUS: Stage 2.6 #########")
    # Reconfigure bonus question at will
    # Robot extract documentation: http://robot.obolibrary.org/extract
    # jar_location: full path that robor.jar file exists
    # method: method used from robot API, Options: BOT, TOP, STAR
    # input_location: full path that the initial .owl file exists
    # term_location: full path that the term file exists
    # output location: full path and new file name that the produced .owl file will be placed
    get_Smodule(jar_location='/home/skalogerakis/Documents/Workspace/CS567/MyDocs/robot.jar',
                method='BOT',
                input_location='/home/skalogerakis/Documents/Workspace/CS567/main_final_onto.owl',
                term_location='/home/skalogerakis/Documents/Workspace/CS567/Robot/term_sample.txt',
                output_location='/home/skalogerakis/Documents/Workspace/CS567/Robot/bonus_final_onto.owl')
    print("Completed file generation")
