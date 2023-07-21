from enum import Enum, IntEnum
from pydantic import BaseModel, Field


class FamilyStatus(str, Enum):
    Single = "Single / not married"
    Married = "Married"
    Civil_marriage = "Civil marriage"
    Separated = "Separated"
    Widow = "Widow"


class HousingType(str, Enum):
    House_apartment = "House / apartment"
    With_parents = "With parents"
    Municipal_apartment = "Municipal apartment"
    Rented_apartment = "Rented apartment"
    Office_apartment = "Office apartment"
    Co_op_apartment = "Co-op apartment"


class EducationType(str, Enum):
    Secondary_secondary_special = "Secondary / secondary special"
    Higher_education = "Higher education"
    Incomplete_higher = "Incomplete higher"
    Lower_secondary = "Lower secondary"
    Academic_degree = "Academic degree"


class OccupationType(str, Enum):
    Laborers = "Laborers"
    Core_staff = "Core staff"
    Accountants = "Accountants"
    Managers = "Managers"
    Drivers = "Drivers"
    Sales_staff = "Sales staff"
    Cleaning_staff = "Cleaning staff"
    Cooking_staff = "Cooking staff"
    Private_service_staff = "Private service staff"
    Medicine_staff = "Medicine staff"
    Security_staff = "Security staff"
    High_skill_tech_staff = "High skill tech staff"
    Waiters_barmen_staff = "Waiters/barmen staff"
    Low_skill_Laborers = "Low-skill Laborers"
    Realty_agents = "Realty agents"
    Secretaries = "Secretaries"
    IT_staff = "IT staff"
    HR_staff = "HR staff"
    Other_occupation = "Other"


class OrganizationType(str, Enum):
    Business = "Business"
    School = "School"
    Government = "Government"
    Religion = "Religion"
    Other_organization = "Other"
    Electricity = "Electricity"
    Medicine = "Medicine"
    Self_employed = "Self-employed"
    Transport = "Transport"
    Construction = "Construction"
    Housing = "Housing"
    Kindergarten = "Kindergarten"
    Trade = "Trade"
    Industry = "Industry"
    Military = "Military"
    Services = "Services"
    Security_Ministries = "Security Ministries"
    Emergency = "Emergency"
    Security = "Security"
    University = "University"
    Police = "Police"
    Postal = "Postal"
    Agriculture = "Agriculture"
    Restaurant = "Restaurant"
    Culture = "Culture"
    Hotel = "Hotel"
    Bank = "Bank"
    Insurance = "Insurance"
    Mobile = "Mobile"
    Legal_Services = "Legal Services"
    Advertising = "Advertising"
    Cleaning = "Cleaning"
    Telecom = "Telecom"
    Realtor = "Realtor"


class IncomeType(str, Enum):
    Student = "Student"
    Working = "Working"
    Commercial_associate = "Commercial associate"
    State_servant = "State servant"
    Pensioner = "Pensioner"
    Unemployed = "Unemployed"


class Validation(BaseModel):
    SURNAME: str = Field(default="Undefined", min_length=3, max_length=20)
    NAME: str = Field(default="Undefined", min_length=3, max_length=20)
    PATRONYMIC: str = Field(default="Undefined", min_length=3, max_length=20)
    # TODO:
    CODE_GENDER: str
    # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
    DAYS_BIRTH: int
    # DAYS_BIRTH: str
    PASSPORT: str

    NAME_FAMILY_STATUS: FamilyStatus
    CNT_CHILDREN: int
    NAME_HOUSING_TYPE: HousingType
    FLAG_OWN_CAR: str
    NAME_EDUCATION_TYPE: EducationType
    #
    OCCUPATION_TYPE: OccupationType
    ORGANIZATION_TYPE: OrganizationType
    # # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
    DAYS_EMPLOYED: int
    # DAYS_EMPLOYED: str
    NAME_INCOME_TYPE: IncomeType
    # # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
    AMT_INCOME_TOTAL: float
    # "AMT_INCOME_TOTAL": str(float(self.income_total.input.value) / 2),
    #
    AMT_CREDIT: int
    # # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
    AMT_ANNUITY: float
    # "AMT_ANNUITY": str(float(self.credit.input.value) / int(self.months.input.value))
    MONTHS_CREDIT: int
