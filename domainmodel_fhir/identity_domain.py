from pyelt.datalayers.database import Columns
from pyelt.datalayers.dv import DvEntity, Sat, Link, HybridSat, HybridLink, LinkReference


#########################################################################################################
#                                                                                                       #
# Domein model volgens FHIR-standaard (hl7.org.fhir). Iedere Entiteit heeft als type "DomainResource"   #
#                                                                                                       #
#########################################################################################################


##### INDIVIDUALS #####

class GenderTypes:
    """enum met codes"""
    male = 'male'
    female = 'female'
    other = 'other'
    unknown = 'unknown'

# https://www.hl7.org/fhir/patient.html

class Patient(DvEntity):
    class Default(Sat):
        active = Columns.BoolColumn()
        gender = Columns.TextColumn(default_value=GenderTypes.unknown)
        birthdate = Columns.DateColumn()
        deceased_boolean = Columns.BoolColumn()
        deceased_datetime = Columns.DateTimeColumn()
        marital_status = Columns.FHIR.CodeableConceptColumn()
        multiple_birth_boolean = Columns.BoolColumn()
        multiple_birth_integer = Columns.IntColumn()

    class Identifier(HybridSat):
        class Types(HybridSat.Types):
            usual = 'usual'
            official = 'official'
            temp = 'temp'
            secondary = 'secondary (If known)'
        use = Columns.TextColumn(default_value=Types.official)
        id_type = Columns.FHIR.CodeableConceptColumn()
        system = Columns.TextColumn()
        value = Columns.TextColumn()
        period = Columns.FHIR.PeriodColumn()

    # https://simplifier.net/NL-BasicComponents/nl-core-humanname
    class Name(HybridSat):
        class Types(HybridSat.Types):
            usual = 'usual'
            official = 'official'
            temp = 'temp'
            nickname = 'nickname'
            anonymous = 'anonymous'
            old = 'old'
            maiden = 'maiden'
            none = ''
        use = Columns.TextColumn(default_value=Types.none)
        text = Columns.TextColumn()
        family = Columns.TextArrayColumn()
        given = Columns.TextArrayColumn()
        prefix = Columns.TextArrayColumn()
        suffix = Columns.TextArrayColumn()
        period = Columns.FHIR.PeriodColumn()

    class Telecom(HybridSat):
        class Types(HybridSat.Types):
            home = 'home'
            work = 'work'
            temp = 'temp'
            old = 'old'
            mobile = 'mobile'
        class Systems():
            phone = 'phone'
            fax = 'fax'
            email = 'email'
            pager = 'pager'
            other = 'other'

        use = Columns.TextColumn()
        system = Columns.TextColumn()
        value = Columns.TextColumn()
        rank = Columns.IntColumn()
        period = Columns.FHIR.PeriodColumn()

    class Address(HybridSat):
        class Types(HybridSat.Types):
            home = 'home'
            work = 'work'
            temp = 'temp'
            old = 'old'

        class AddressTypes():
            postal = 'postal'
            physical = 'physical'
            both = 'both'

        use= Columns.TextColumn()
        add_type = Columns.TextColumn()
        text = Columns.TextColumn()
        line = Columns.TextArrayColumn()
        city = Columns.TextColumn()
        district = Columns.TextColumn()
        state = Columns.TextColumn()
        postalcode = Columns.TextColumn()
        country = Columns.TextColumn()
        period = Columns.FHIR.PeriodColumn()

    class Communication(Sat):
        language = Columns.FHIR.CodeableConceptColumn()
        preffered = Columns.BoolColumn()

    class Extra(Sat):
        # contactpersoon
        contact = Columns.JsonColumn()
        # mag weg
        animal = Columns.JsonColumn()
        photo = Columns.TextColumn()

class PatientManagingOrganizationLink(Link):
    patient = LinkReference(Patient)
    organization = LinkReference(Organization)

class PatientCareProviderLink(Link):
    patient = LinkReference(Patient)
    practioner = LinkReference(Practitioner)
    organization = LinkReference(Organization)


##### GROUPS #####

class Organization(DvEntity):
    class Default(Sat):
        active = Columns.BoolColumn()
        name = Columns.TextColumn()

    class Identifier(HybridSat):
        class Types(HybridSat.Types):
            usual = 'usual'
            official = 'official'
            temp = 'temp'
            secondary = 'secondary (If known)'

        use = Columns.TextColumn(default_value=Types.official)
        org_type = Columns.FHIR.CodeableConceptColumn()
        system = Columns.TextColumn()
        value = Columns.TextColumn()
        period = Columns.FHIR.PeriodColumn()

    #todo: afmaken mat andere sats

class OrganizationOrganizationLink(Link):
    organization = LinkReference(Organization)
    linked_to_organization = LinkReference(Organization)


# https://www.hl7.org/fhir/practitioner.html
# https://simplifier.net/Nictiz/bgz-Practitioner
class Practitioner(DvEntity):
    pass




# Organisatie: https://simplifier.net/Nictiz/bgz-Organization
# Zorgaanbieder: https://simplifier.net/Nictiz/bgz-CareProvider
#
#
# Zorgverzekeraar : https://www.hl7.org/fhir/coverage.html
# Afdeling : https://simplifier.net/Nictiz/bgz-DepartmentType
#
# Zorgactiviteit : https://www.hl7.org/fhir/episodeofcare.html
# Traject / subtraject :  https://www.hl7.org/fhir/episodeofcare.html
#
# Contact : https://www.hl7.org/fhir/encounter.html
# Afspraak: https://www.hl7.org/fhir/appointment.html
# Labresult: https://www.hl7.org/fhir/observation.html
#
# https://simplifier.net/NL-BasicComponents/nl-core-humanname
