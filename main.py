from typing import Union

from owlready2 import *

onto = get_ontology("http://skalerakis.org/onto.owl")
# TODO can we do better for rule 1)?????
'''
    1) Satellite is equivalent to Artificial Satellite or Natural Satellite.
'''


class Satellite(Thing):
    namespace = onto


class NaturalSatellite(Satellite):
    namespace = onto


class ArtificialSatellite(Satellite):
    namespace = onto
    is_a = [
        Not(NaturalSatellite)]  # 2) Artificial Satellite is not a natural satellite.


NaturalSatellite.is_a.append(Not(ArtificialSatellite))  # 3) Natural Satellite in not an artificial satellite
# TODO add dark matter by doing the same as satellites. Maybe Add Matter that is a superset of dark and normal matter

'''
    This is the key for rule 1)
    In ontologies an individual can belong to several classes. Therefore, a
    given satellite can very well be both Natural and Artificial.(Open World Assumption)
    For that reason, declare classes as disjoint. These cannot have individuals in common!!
    So the result will be either Natural or Artificial Satellite
'''
AllDisjoint([ArtificialSatellite, NaturalSatellite])
Satellite.equivalent_to.append(Or([ArtificialSatellite ,NaturalSatellite]))


#
# class Galaxy(Thing):
#     namespace = onto
#
#
# # TODO this is for functional property -> Check that
# class hasCenterOfMass(Galaxy >> int, FunctionalProperty):
#     namespace = onto
#
# # The following two are used to for the inverse roles
# class hasForSatellite():
#     pass
#
# class isSatelliteOf():
#     inverse = hasForSatellite
#
# # Definition for symmetric properties
# class pullGravity(ObjectProperty, SymmetricProperty):
#     # domain =
#     # range =
#     pass

# Essentially by this way, we can define that If something is a satellite then it orbits
# isSatellileOf is a subclass of orbitsAround
# class orbitsAround():
#
# class isSatelliteOf(orbitsAround):
#     inverse = hasForSatellite


class CelestialBody(Thing):
    namespace = onto


class Galaxy(Thing):
    namespace = onto


# 4) A CelestialBody is located in a Galaxy
class locatedIn(ObjectProperty):
    namespace = onto
    domain = [CelestialBody]
    range = [Galaxy]


class observes(ObjectProperty):
    namespace = onto
    domain = [CelestialBody]    #or Thing
    range = [CelestialBody]

# 5) A space telescope is a celestial body that observes other celestial body
class SpaceTelescope(CelestialBody):
    namespace = onto
    is_a = [CelestialBody & observes.some(CelestialBody)]

class orbitsAround():
    namespace = onto

# TODO all the Thing Concepts must be disjoint
if __name__ == '__main__':
    # print(locatedIn.domain)

    print('Satellite subclasses ', [x for x in Satellite.subclasses()])

    print("Is a ART ", ArtificialSatellite.is_a)
    print("Is a NAT ", NaturalSatellite.is_a)
    print("Desc ", NaturalSatellite.descendants())
    print("Ans ", ArtificialSatellite.ancestors())

    onto.save(file="sk_onto.owl", format="rdfxml")
