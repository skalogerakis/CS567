# Owlready2 API


## Classes and Individual(Instances)

### Creating a Class

A new Class can be created in an ontology by inheriting the owlready2.Thing class.

The ontology class attribute can be used to associate your class to the given ontology. If not specified, this attribute is inherited from the parent class (in the example below, the parent class is Thing, which is defined in the ‘owl’ ontology).

    >>> from owlready2 import *

    >>> onto = get_ontology("http://test.org/onto.owl")

    >>> class Drug(Thing):
    ...     namespace = onto
    
    
The namespace Class attribute is used to build the full IRI of the Class, and can be an ontology or a namespace (see Namespaces). The ‘with’ statement can also be used to provide the ontology (or namespace):

    >>> onto = get_ontology("http://test.org/onto.owl")

    >>> with onto:
    ...     class Drug(Thing):
    ...         pass
    
The .iri attribute of the Class can be used to obtain the full IRI of the class.

    >>> print(Drug.iri)
    http://test.org/onto.owl#Drug
    
.name and .iri attributes are writable and can be modified (this allows to change the IRI of an entity, which is sometimes called “refactoring”).


### Creating and managing subclasses

Subclasses can be created by inheriting an ontology class. Multiple inheritance is supported.

    >>> class DrugAssociation(Drug): # A drug associating several active principles
    ...     pass
    
Owlready2 provides the .is_a attribute for getting the list of superclasses (__bases__ can be used, but with some limits described in Class constructs, restrictions and logical operators). It can also be modified for adding or removing superclasses.

    >>> print(DrugAssociation.is_a)
    [onto.Drug]

The .subclasses() method returns the list of direct subclasses of a class.

    >>> print(Drug.subclasses())
    [onto.DrugAssociation]
    
The .descendants() and .ancestors() Class methods return a set of the descendant and ancestor Classes (including self, but excluding non-entity classes such as restrictions).

    >>> DrugAssociation.ancestors()
    {onto.DrugAssociation, owl.Thing, onto.Drug}


### Creating classes dynamically
The ‘types’ Python module can be used to create classes and subclasses dynamically:

    >>> import types

    >>> with my_ontology:
    ...     NewClass = types.new_class("NewClassName", (SuperClass,))

### Creating equivalent classes

The .equivalent_to Class attribute is a list of equivalent classes. It behaves like .is_a (programmatically).

To obtain all equivalent classes, including indirect ones (due to transitivity), use .INDIRECT_equivalent_to.

### Creating Individuals
Individuals are instances in ontologies. They are created as any other Python instances. The first parameter is the name (or identifier) of the Individual; it corresponds to the .name attribute in Owlready2. If not given, the name if automatically generated from the Class name and a number.

    >>> my_drug = Drug("my_drug")
    >>> print(my_drug.name)
    my_drug
    >>> print(my_drug.iri)
    http://test.org/onto.owl#my_drug

    >>> unamed_drug = Drug()
    >>> print(unamed_drug.name)
    drug_1


Additional keyword parameters can be given when creating an Individual, and they will be associated to the corresponding Properties (for more information on Properties, see Properties).

    my_drug = Drug("my_drug2", namespace = onto, has_for_active_principle = [],...)

The Instances are immediately available in the ontology:

    >>> print(onto.drug_1)
    onto.drug_1

The .instances() class method can be used to iterate through all Instances of a Class (including its subclasses). It returns a generator.

    >>> for i in Drug.instances(): print(i)
    
Multiple calls with the individual name and namespace will returns the same individual (without creating a dupplicate), and update the individual if property values are given.

    >>> assert Drug("my_drug3") is Drug("my_drug3")
 
Finally, Individuals also have the .equivalent_to attribute (which correspond to the “same as” relation).

### Querying Individual relations

For a given Individual, the values of a property can be obtained with the usual “object.property” dot notation. See Properties for more details.

    >>> print(onto.my_drug.has_for_active_principle)
    
Property name can be prefixed with “INDIRECT_” to obtain all indirect relations (i.e. those asserted at the class level with restriction, implied by transistive properties, subproperties, equivalences, etc):

    >>> print(onto.my_drug.INDIRECT_has_for_active_principle)
    
    
### Introspecting Individuals
The list of properties that exist for a given individual can be obtained by the .get_properties() method. It returns a generator that yields the properties (without dupplicates).

    >>> onto.drug_1.get_properties()
    
The following example shows how to list the properties of a given individual, and the associated values:

    >>> for prop in onto.drug_1.get_properties():
    >>>     for value in prop[onto.drug_1]:
    >>>         print(".%s == %s" % (prop.python_name, value))
    
Notice the “Property[individual]” syntax. It allows to get the values as a list, even for functional properties (contrary to getattr(individual, Property.python_name).

Inverse properties can be obtained by the .get_inverse_properties() method. It returns a generator that yields (subject, property) tuples.

    >>> onto.drug_1.get_inverse_properties()
    

### Mutli-Class Individuals
In ontologies, an Individual can belong to more than one Class. This is supported in Owlready2.

Individuals have a .is_a atribute that behaves similarly to Class .is_a, but with the Classes of the Individual. In order to create a mutli-Class Individual, you need to create the Individual as a single-Class Instance first, and then to add the other Class(ses) in its .is_a attribute:

    >>> class BloodBasedProduct(Thing):
    ...     ontology = onto

    >>> a_blood_based_drug = Drug()
    >>> a_blood_based_drug.is_a.append(BloodBasedProduct)
    
Owlready2 will automatically create a hidden Class that inherits from both Drug and BloodBasedProduct. This hidden class is visible in a_blood_based_drug.__class__, but not in a_blood_based_drug.is_a.

### Equivalent (identical, SameAs) individuals
The .equivalent_to Individual attribute is a list of equivalent individuals (corresponding to OWL SameAs relation). This list can be modified.

To obtain all equivalent individuals, including indirect ones (due to transitivity), use .INDIRECT_equivalent_to.

### Destroying entities
The destroy_entity() global function can be used to destroy an entity, i.e. to remove it from the ontology and the quad store. Owlready2 behaves similarly to Protege4 when destroying entities: all relations involving the destroyed entity are destroyed too, as well as all class constructs and blank nodes that refer it.

    >>> destroy_entity(individual)
    >>> destroy_entity(Klass)
    >>> destroy_entity(Property)

## Properties

### Creating a new class of property
A new property can be created by sublcassing the ObjectProperty or DataProperty class. The ‘domain’ and ‘range’ properties can be used to specify the domain and the range of the property. Domain and range must be given in list, since OWL allows to specify several domains or ranges for a given property (if multiple domains or ranges are specified, the domain or range is the intersection of them, i.e. the items in the list are combined with an AND logical operator).

The following example creates two Classes, Drug and Ingredient, and then an ObjectProperty that relates them.

    >>> from owlready2 import *

    >>> onto = get_ontology("http://test.org/onto.owl")

    >>> with onto:
    ...     class Drug(Thing):
    ...         pass
    ...     class Ingredient(Thing):
    ...         pass
    ...     class has_for_ingredient(ObjectProperty):
    ...         domain    = [Drug]
    ...         range     = [Ingredient]
    
In addition, the ‘domain >> range’ syntax can be used when creating property. It replaces the ObjectProperty or DataProperty parent Class, as follows:

    >>> with onto:
    ...     class has_for_ingredient(Drug >> Ingredient):
    ...         pass
    
    
In addition, the following subclasses of Property are available: FunctionalProperty, InverseFunctionalProperty, TransitiveProperty, SymmetricProperty, AsymmetricProperty, ReflexiveProperty, IrreflexiveProperty. They should be used in addition to ObjectProperty or DataProperty (or the ‘domain >> range’ syntax).

    Getting domain and range
    
The .domain and .range attributes of a Property can be used to query its domain and range. They returns a list.

    >>> has_for_ingredient.domain
    [Drug]

    >>> has_for_ingredient.range
    [Ingredient]
    
### Creating a relation
A relation is a triple (subject, property, object) where property is a Property class, and subject and object are instances (or literal, such as string or numbers) which are subclasses of the domain and range defined for the property class. A relation can be get or set using Python attribute of the subject, the attribute name being the same as the Property class name:

    >>> my_drug = Drug("my_drug")

    >>> acetaminophen = Ingredient("acetaminophen")

    >>> my_drug.has_for_ingredient = [acetaminophen]
    
The attribute contains a list of the subjects:

    >>> print(my_drug.has_for_ingredient)
    [onto.acetaminophen]
This list can be modifed in place or set to a new value; Owlready2 will automatically add or delete RDF triples in the quadstore as needed:

    >>> codeine = Ingredient("codeine")

    >>> my_drug.has_for_ingredient.append(codeine)

    >>> print(my_drug.has_for_ingredient)
    [onto.acetaminophen, onto.codeine]
    
### Data Property
Data Properties are Properties with a data type in their range. The following data types are currently supported by Owlready2:

- int
- float
- bool
- str (string)
- owlready2.normstr (normalized string, a single-line string)
- owlready2.locstr (localized string, a string with a language associated)
- datetime.date
- datetime.time
- datetime.datetime


Here is an example of a string Data Property:

    >>> with onto:
    ...     class has_for_synonym(DataProperty):
    ...         range = [str]

    >>> acetaminophen.has_for_synonym = ["acetaminophen", "paracétamol"]
    
The ‘domain >> range’ syntax can also be used:

    >>> with onto:
    ...     class has_for_synonym(Thing >> str):
    ...         pass
    

### Inverse Properties
Two properties are inverse if they express the same meaning, but in a reversed way. For example the ‘is_ingredient_of’ Property is the inverse of the ‘has_for_ingredient’ Property created above: saying “a drug A has for ingredient B” is equivalent to “B is ingredient of drug A”.

In Owlready2, inverse Properties are defined using the ‘inverse_property’ attribute.

    >>> with onto:
    ...     class is_ingredient_of(ObjectProperty):
    ...         domain           = [Ingredient]
    ...         range            = [Drug]
    ...         inverse_property = has_for_ingredient
    
 
Owlready automatically handles Inverse Properties. It will automatically set has_for_ingredient.inverse_property, and automatically update relations when the inverse relation is modified.

    >>> my_drug2 = Drug("my_drug2")

    >>> aspirin = Ingredient("aspirin")

    >>> my_drug2.has_for_ingredient.append(aspirin)

    >>> print(my_drug2.has_for_ingredient)
    [onto.aspirin]

    >>> print(aspirin.is_ingredient_of)
    [onto.my_drug2]


    >>> aspirin.is_ingredient_of = []

    >>> print(my_drug2.has_for_ingredient)
    []
    
**Note**

This won’t work for the drug created previously, because we created the inverse property after we created the relation between my_drug and acetaminophen.

### Functional and Inverse Functional properties
A functional property is a property that has a single value for a given instance. Functional properties are created by inheriting the FunctionalProperty class.

    >>> with onto:
    ...     class has_for_cost(DataProperty, FunctionalProperty): # Each drug has a single cost
    ...         domain    = [Drug]
    ...         range     = [float]

    >>> my_drug.has_for_cost = 4.2

    >>> print(my_drug.has_for_cost)
    4.2
    
Contrary to other properties, a functional property returns a single value instead of a list of values. If no value is defined, they returns None.

    >>> print(my_drug2.has_for_cost)
    None
    
Owlready2 is also able to guess when a Property is functional with respect to a given class. In the following example, the ‘prop’ Property is not functional, but Owlready2 guesses that, for Individuals of Class B, there can be only a single value. Consequently, Owlready2 considers prop as functional for Class B.

    >>> with onto:
    ...     class prop(ObjectProperty): pass
    ...     class A(Thing): pass
    ...     class B(Thing):
    ...         is_a = [ prop.max(1) ]

    >>> A().prop
    []
    >>> B().prop
    None
    
An Inverse Functional Property is a property whose inverse property is functional. They are created by inheriting the InverseFunctionalProperty class.

### Creating a subproperty
A subproperty can be created by subclassing a Property class.

    >>> with onto:
    ...     class ActivePrinciple(Ingredient):
    ...         pass
    ...     class has_for_active_principle(has_for_ingredient):
    ...         domain    = [Drug]
    ...         range     = [ActivePrinciple]

**Note**

Owlready2 currently does not automatically update parent properties when a child property is defined. This might be added in a future version, though.

### Obtaining indirect relations (considering subproperty, transitivity, etc)
Property name can be prefixed by “INDIRECT_” to obtain all indirectly related entities. It takes into account:

- transitive, symmetric and reflexive properties,
- property inheritance (i.e. subproperties),
- classes of an individual (i.e. values asserted at the class level),
- class inheritance (i.e. parent classes).
- equivalences (i.e. equivalent classes, identical “same-as” individuals,…)

      >>> with onto:
      ...     class BodyPart(Thing): pass
      ...     class part_of(BodyPart >> BodyPart, TransitiveProperty): pass
      ...     abdomen          = BodyPart("abdomen")
      ...     heart            = BodyPart("heart"           , part_of = [abdomen])
      ...     left_ventricular = BodyPart("left_ventricular", part_of = [heart])
      ...     kidney           = BodyPart("kidney"          , part_of = [abdomen])

      ... print(left_ventricular.part_of)
      [heart]

      ... print(left_ventricular.INDIRECT_part_of)
      [heart, abdomen]
      
### Associating Python alias name to Properties
In ontologies, properties are usually given long names, e.g. “has_for_ingredient”, while in programming languages like Python, shorter attribute names are more common, e.g. “ingredients” (notice also the use of a plural form, since it is actually a list of several ingredients).

Owlready2 allows to rename Properties with more Pythonic name through the ‘python_name’ annotation (defined in the Owlready ontology, file ‘owlready2/owlready_ontology.owl’ in Owlready2 sources, URI http://www.lesfleursdunormal.fr/static/_downloads/owlready_ontology.owl):

    >>> has_for_ingredient.python_name = "ingredients"

    >>> my_drug3 = Drug()

    >>> cetirizin = Ingredient("cetirizin")

    >>> my_drug3.ingredients = [cetirizin]
    
**Note**

The Property class is still considered to be called ‘has_for_ingredient’, for example it is still available as ‘onto.has_for_ingredient’, but not as ‘onto.ingredients’.

For more information about the use of annotations, see Annotations.

The ‘python_name’ annotations can also be defined in ontology editors like Protégé, by importing the Owlready ontology (file ‘owlready2/owlready_ontology.owl’ in Owlready2 sources, URI http://www.lesfleursdunormal.fr/static/_downloads/owlready_ontology.owl).

### Getting relation instances
The list of relations that exist for a given property can be obtained by the .get_relations() method. It returns a generator that yields (subject, object) tuples.

      >>> onto.has_for_active_principle.get_relations()

**Warning**

The quadstore is not indexed for the .get_relations() method. Thus, it can be slow on huge ontologies.
