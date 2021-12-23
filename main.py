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

class hasOrbitingAround(ObjectProperty): # helpful to insert multiple instances that orbit around in abox
    namespace = onto
    inverse_property = orbitsAround  # 21) hasOrbitingAround is equivalent to the Inverse of orbitsAround

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


class PlanetarySystemBody(Thing):
    namespace = onto
    is_a = [CelestialBody & Not(Planet) & Not(DwarfPlanet) & Not(
        NaturalSatellite)]  # 3) A planetary system Body is a celestial body
    # that is not a planet nor a dwarf planet not a satellite


class SpaceTelescope(Thing):
    namespace = onto
    is_a = [CelestialBody & observes.some(
        CelestialBody)]  # 10) A space telescope is a celestial body that observes some celestial body


class Comet(PlanetarySystemBody):  # 11) Comet is a planetary system body (is a subclass of)
    namespace = onto


class Asteroid(PlanetarySystemBody):  # 12) Asteroid is a planetary system body (is a subclass of)
    namespace = onto

# All together it corresponds to the rule: Comet OR Asteroid IS_A PlanetarySystemBody
# (hence we use somewhere the concept PlanetarySystemBody) [to delete this]


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
    milkyway = Galaxy("Milkyway")
    andromeda = Galaxy("Andromeda")
    cygunus = Galaxy("Cygunus")

    # Celestial Body Concepts
    CelestialBody("Moon")
    CelestialBody("Sun")
    CelestialBody("Earth")
    CelestialBody("Mars")
    CelestialBody("Pluto")

    # Planetary System Body
    PlanetarySystemBody("Ceres") # Ceres is an Asteroid
    PlanetarySystemBody("Enke") # Enke is a Comet
    PlanetarySystemBody("Halleys") # Halleys is a Comet
    PlanetarySystemBody("Icarus") # Icarus is an Asteroid

    # Planet
    earth = Planet("Earth")
    mars = Planet("Mars")
    jupiter = Planet("Jupiter")
    venus = Planet("Venus")
    saturn = Planet("Saturn")

    # Star
    sun = Star("Sun")
    sirius = Star("Sirius")
    rigel = Star("Rigel")
    pleiades = Star("Pleiades")

    # Dwarf Planet
    pluto = DwarfPlanet("Pluto")
    makemake = DwarfPlanet("Makemake")
    eris = DwarfPlanet("Eris")

    # Asteroid
    ceres = Asteroid("Ceres")
    eros = Asteroid("Eros")
    icarus = Asteroid("Icarus")
    pallas = Asteroid("Pallas")

    # Natural Satellite
    moon = NaturalSatellite("Moon")
    europa = NaturalSatellite("Europa")
    triton = NaturalSatellite("Triton")
    rhea = NaturalSatellite("Rhea")
    dione = NaturalSatellite("Dione")

    # Artificial Satellite
    sputnik = ArtificialSatellite("Sputnik")
    glory = ArtificialSatellite("Glory")
    aura = ArtificialSatellite("Aura")
    stereo = ArtificialSatellite("STEREO")

    # Space Telescope
    hubble = SpaceTelescope("Hubble")
    most = SpaceTelescope("MOST")
    euve = SpaceTelescope("EUVE")

    # Comet
    chiron = Comet("Chiron")
    borrelly = Comet("Borrelly")
    halley = Comet("Halley")
    enke = Comet("Enke")

    # Matter
    normal_matter = NormalMatter("MilkywayNM")
    dark_matter = DarkMatter("MilkywayDM")

    # Relations between concepts and roles

    milkyway.hasMember = [sun, sirius, rigel, earth, mars, jupiter, venus, saturn, pluto, 
    moon, europa, triton, eros, pallas, icarus, ceres]

    milkyway.hasCenterOfMass = Thing
    andromeda.hasCenterOfMass = Thing
    cygunus.hasCenterOfMass = Thing

    earth.pullGravity = [moon, sun, hubble, sputnik]
    sun.pullGravity = [earth, mars, jupiter, venus, saturn, icarus]

    normal_matter.pullGravity.append(dark_matter)

    saturn.hasForSatellite = [rhea, dione]
    earth.hasForSatellite = [moon, aura, sputnik]

    hubble.orbitsAround.append(earth)
    moon.orbitsAround.append(earth)
    sputnik.orbitsAround.append(earth)

    # earth.hasOrbitingAround = [moon, sputnik, hubble]
    sun.hasOrbitingAround = [earth, mars, jupiter, venus, saturn, pluto]

    hubble.observes.append(earth)
    most.observes.append(earth)
    euve.observes.append(milkyway)


    onto.save(file="mar_onto.owl", format="rdfxml")
