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
    gal1 = Galaxy("Milkyway")
    gal2 = Galaxy("Andromeda")
    gal3 = Galaxy("Cygunus")

    # Celestial Body Concepts
    cel1 = CelestialBody("Moon")
    cel2 = CelestialBody("Sun")
    cel3 = CelestialBody("Mars")
    cel4 = CelestialBody("Pluto")

    # Planetary System Body
    psb1 = PlanetarySystemBody("Enke")
    psb2 = PlanetarySystemBody("Haleys")
    psb3 = PlanetarySystemBody("Ceres")
    psb4 = PlanetarySystemBody("Icarus")

    # Planet
    pl1 = Planet("Earth")
    pl2 = Planet("Mars")
    pl3 = Planet("Jupiter")
    pl4 = Planet("Venus")
    pl5 = Planet("Saturn")

    # Star
    st1 = Star("Sun")
    st2 = Star("Sirius")
    st3 = Star("Rigel")
    st4 = Star("Pleiades")

    # Dwarf Planet
    dp1 = DwarfPlanet("Ceres")
    dp2 = DwarfPlanet("Pluto")
    dp3 = DwarfPlanet("Makemake")
    dp4 = DwarfPlanet("Eris")

    # Asteroid
    ast1 = Asteroid("Eros")
    ast2 = Asteroid("Ceres")
    ast3 = Asteroid("Icarus")
    ast4 = Asteroid("Pallas")

    # Natural Satellite
    ns1 = NaturalSatellite("Moon")
    ns2 = NaturalSatellite("Europa")
    ns3 = NaturalSatellite("Triton")

    # Artificial Satellite
    as1 = ArtificialSatellite("Sputnik")
    as2 = ArtificialSatellite("Glory")

    # Space Telescope
    sptel1 = SpaceTelescope("Hubble")
    sptel1 = SpaceTelescope("MOST")
    sptel1 = SpaceTelescope("EUVE")

    # Comet
    com1 = Comet("Chiron")
    com2 = Comet("Borrelly")
    com3 = Comet("Halley")
    com4 = Comet("Enke")

    # Combination with roles
    ns1.orbitsAround = [pl1]    # Moon orbitsAround Earth

    # TODO is it obligatory to add roles??? See how this is done
    onto.save(file="skaloger_onto.owl", format="rdfxml")
