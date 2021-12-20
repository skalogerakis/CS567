from owlready2 import *

onto = get_ontology("http://skalerakis.org/onto.owl")


# TODO ask about that, when associating with ArtificialSatellite(Natural Satellite),Is a [onto.NaturalSatellite, Not(onto.NaturalSatellite)]
# When define using ArtificialSatellite(Thing), Is a [owl.Thing, Not(onto.NaturalSatellite)] LOOKS more correct
class NaturalSatellite(Thing):
    namespace = onto


class ArtificialSatellite(Thing):
    namespace = onto
    is_a = [Not(NaturalSatellite)]
    pass





class Galaxy(Thing):
    namespace = onto


class CelestialBody(Thing):
    namespace = onto

# TODO can we do that???? Celestial body that observe other Celestial Body
class observes(ObjectProperty):
    namespace = onto
    domain = [CelestialBody]
    range = [CelestialBody]
    pass

class SpaceTelescope(CelestialBody):
    namespace = onto
    is_a = [CelestialBody & observes.some(CelestialBody)]


class locatedIn(ObjectProperty):
    namespace = onto
    domain = [CelestialBody]
    range = [Galaxy]


if __name__ == '__main__':
    print("Is a", ArtificialSatellite.is_a)
    print([x for x in NaturalSatellite.subclasses()])
    print("Desc ", NaturalSatellite.descendants())
    print("Ans ", ArtificialSatellite.ancestors())
    # print(Galaxy.iri)
    # print(CelestialBody.iri)
    # print(locatedIn.domain)
    # print(locatedIn.range)
    # print(ArtificialSatellite.iri)
    # print(ArtificialSatellite.is_a)
    # print([x for x in NaturalSatellite.subclasses()])
    # print(Professor.iri)
    # print(Person.iri)
    # print(Professor.is_a)
    # print([x for x in Person.subclasses()])
    # print(Professor.ancestors())
    # #
    # bilas = Professor('bilas')
    # print(bilas.iri)
    #
    # giorgos = Student('giorgos')
    # #
    # print(has_advisor.domain)
    #
    # giorgos.has_advisor = [bilas]
    # print(giorgos.has_advisor)

    onto.save(file="sk_onto.owl", format="rdfxml")
