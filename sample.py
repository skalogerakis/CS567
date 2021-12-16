from owlready2 import *

onto = get_ontology("http://test.org/onto.owl")


class Person(Thing):
    namespace = onto

class Professor(Person):
    pass

#
#
#
#
class Course(Thing):
    namespace = onto
    pass

#
class teaches(Professor >> Course):
    namespace = onto
    pass
#
#
#
#
#
#
# class ActiveProfessor(Professor):
#     equivalent_to = [Professor & teaches.some(Course)]
#
#
#
#
#
# class InactiveProfessor(Professor):
#     equivalent_to = [Professor & Not(teaches.some(Course))]
#
#
#
#
#
#
#
#
#
# class Student(Person):
#     pass
#
#
# class has_advisor(ObjectProperty):
#     domain = [Student]
#     range = [Professor]
#


if __name__ == '__main__':

    print(Professor.iri)
    print(Person.iri)
    print(Professor.is_a)
    print([x for x in Person.subclasses()])
    print(Professor.ancestors())
    #
    bilas = Professor('bilas')
    print(bilas.iri)
    #
    # giorgos = Student('giorgos')
    # #
    # print(has_advisor.domain)
    #
    # giorgos.has_advisor = [bilas]
    # print(giorgos.has_advisor)

    onto.save(file= "onto.owl", format = "rdfxml")
