from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import datetime
import os
from pydantic import BaseModel, Field
from enum import Enum, IntEnum
import aiohttp

DEFAULT_FRONTEND_HOST = '127.0.0.1'
DEFAULT_FRONTEND_PORT = '50422'
DEFAULT_DATA_HOST = '127.0.0.1'
DEFAULT_DATA_PORT = '8888'

front_host = os.getenv('FRONTEND_HOST', DEFAULT_FRONTEND_HOST)
front_port = os.getenv('FRONTEND_PORT', DEFAULT_FRONTEND_PORT)
front_addr = f"http://{front_host}:{front_port}/"
data_host = os.getenv('DATA_HOST', DEFAULT_DATA_HOST)
data_port = os.getenv('DATA_PORT', DEFAULT_DATA_PORT)
data_addr = f"http://{data_host}:{data_port}/"

app = FastAPI()

origins = [
    front_addr,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    print('Server started :', datetime.datetime.now())


@app.on_event("shutdown")
async def shutdown_event():
    print('Server shutdown :', datetime.datetime.now())



class FamilyStatus(str, Enum):
    Single = 'Single / not married'
    Married = 'Married'
    Civil_marriage = 'Civil marriage'
    Separated = 'Separated'
    Widow = 'Widow'

class HousingType(str, Enum):
    House_apartment = 'House / apartment'
    With_parents = 'With parents'
    Municipal_apartment = 'Municipal apartment'
    Rented_apartment = 'Rented apartment'
    Office_apartment = 'Office apartment'
    Co_op_apartment = 'Co-op apartment'
class EducationType(str, Enum):
    Secondary_secondary_special = 'Secondary / secondary special'
    Higher_education = 'Higher education'
    Incomplete_higher = 'Incomplete higher'
    Lower_secondary = 'Lower secondary'
    Academic_degree = 'Academic degree'

class OccupationType(str, Enum):
    Laborers = 'Laborers'
    Core_staff = 'Core staff'
    Accountants = 'Accountants'
    Managers = 'Managers'
    Drivers = 'Drivers'
    Sales_staff = 'Sales staff'
    Cleaning_staff = 'Cleaning staff'
    Cooking_staff = 'Cooking staff'
    Private_service_staff = 'Private service staff'
    Medicine_staff = 'Medicine staff'
    Security_staff = 'Security staff'
    High_skill_tech_staff = 'High skill tech staff'
    Waiters_barmen_staff = 'Waiters/barmen staff'
    Low_skill_Laborers = 'Low-skill Laborers'
    Realty_agents = 'Realty agents'
    Secretaries = 'Secretaries'
    IT_staff = 'IT staff'
    HR_staff = 'HR staff'
    Other_occupation = 'Other'

class OrganizationType(str, Enum):
    Business = 'Business'
    School = 'School'
    Government = 'Government'
    Religion = 'Religion'
    Other_organization = 'Other'
    Electricity = 'Electricity'
    Medicine = 'Medicine'
    Self_employed = 'Self-employed'
    Transport = 'Transport'
    Construction = 'Construction'
    Housing = 'Housing'
    Kindergarten = 'Kindergarten'
    Trade = 'Trade'
    Industry = 'Industry'
    Military = 'Military'
    Services = 'Services'
    Security_Ministries = 'Security Ministries'
    Emergency = 'Emergency'
    Security = 'Security'
    University = 'University'
    Police = 'Police'
    Postal = 'Postal'
    Agriculture = 'Agriculture'
    Restaurant = 'Restaurant'
    Culture = 'Culture'
    Hotel = 'Hotel'
    Bank = 'Bank'
    Insurance = 'Insurance'
    Mobile = 'Mobile'
    Legal_Services = 'Legal Services'
    Advertising = 'Advertising'
    Cleaning = 'Cleaning'
    Telecom = 'Telecom'
    Realtor = 'Realtor'

class IncomeType(str, Enum):
    Student = 'Student'
    Working = 'Working'
    Commercial_associate = 'Commercial associate'
    State_servant = 'State servant'
    Pensioner = 'Pensioner'
    Unemployed = 'Unemployed'

class Gender(str, Enum):
    male = 'M'
    female= 'F'



class Validation(BaseModel):

    SURNAME: str = Field(default="Undefined", min_length=3, max_length=20)
    NAME: str = Field(default="Undefined", min_length=3, max_length=20)
    PATRONYMIC: str = Field(default="Undefined", min_length=3, max_length=20)
    # TODO:
    CODE_GENDER: Gender
    # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
    DAYS_BIRTH: int = Body( ge=7550, lt=25500) # старше 21 и
    PASSPORT: str  = Body(min_length=10, max_length=10)

    NAME_FAMILY_STATUS: FamilyStatus
    CNT_CHILDREN: int = 0
    NAME_HOUSING_TYPE: HousingType
    FLAG_OWN_CAR: str
    NAME_EDUCATION_TYPE: EducationType
    #
    OCCUPATION_TYPE: OccupationType
    ORGANIZATION_TYPE: OrganizationType
    # # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
    DAYS_EMPLOYED: int = 0

    NAME_INCOME_TYPE: IncomeType
    # # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
    AMT_INCOME_TOTAL: float
    # 'AMT_INCOME_TOTAL': str(float(self.income_total.input.value) / 2),
    #
    AMT_CREDIT: int = 0
    # # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
    AMT_ANNUITY: float = 0
    # 'AMT_ANNUITY': str(float(self.credit.input.value) / int(self.months.input.value))
    # test1111
@app.post('/')
async def post_on_ml(info: Validation):
    # Шаг 1: Прием валидированных данных info: Validation
    print(info)

    print('VADKIM\t')
    print(info.json())

    # Шаг 2: Асинхронная отправка POST-запроса к другому приложению ML
    async with aiohttp.ClientSession() as session:
        async with session.post(data_addr) as response:
            result = await response.text()
            print('POST to DATA:', result)
            return 'SUCCESS'



if __name__ == '__main__':
    uvicorn.run(app, reload=True)
