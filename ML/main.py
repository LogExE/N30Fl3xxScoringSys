import uvicorn
from fastapi import FastAPI
import pandas as pd
import json
from pydantic import BaseModel, Field, ValidationError
from val import Validation
import re
import pickle
import warnings
warnings.filterwarnings("ignore")

# нужно установить пакеты lightgbm и scikit-learn
# pip install lightgbm
# pip install scikit-learn

# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}


def main_def():



    # print(type(input_json))
    # try:
    #     data = Validation.model_validate_json(input_json)
    # except ValidationError as e:
    #     print("Exception", e.json())
    # else:
    #     print(data.MONTHS_CREDIT)



    # чтение данных из JSON файла (важно, чтобы в файле были двойные кавычки)
    # и формирование дата фрейма
    df = pd.DataFrame([pd.read_json("data.json", typ="series")])
    # print(df)

    # это таблица-шаблон со всеми столбцами
    pattern = pd.read_csv("app_file.csv")
    # print(pattern)

    # добавление новых признаков и изменение старых
    df = mapping(df)


    # выравнивание таблиц по признакам
    df, _ = df.align(pattern, join='outer', axis=1)

    # расположение столбцов в нужном для модели порядке
    df = df[['CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'MONTHS_CREDIT', 'OWN_CAR', 'IS_MEN',
         'IS_FEMALE', 'AGE', 'EXPERIENCE', 'CREDIT_INCOME_PERCENT', 'ANNUITY_INCOME_PERCENT', 'CREDIT_TERM',
         'EXPERIENCE_PERCENT', 'EDUCATION', 'NAME_INCOME_TYPE_Businessman', 'NAME_INCOME_TYPE_Commercialassociate',
         'NAME_INCOME_TYPE_Maternityleave', 'NAME_INCOME_TYPE_Pensioner', 'NAME_INCOME_TYPE_Stateservant',
         'NAME_INCOME_TYPE_Student', 'NAME_INCOME_TYPE_Unemployed', 'NAME_INCOME_TYPE_Working',
         'NAME_FAMILY_STATUS_Civilmarriage', 'NAME_FAMILY_STATUS_Married', 'NAME_FAMILY_STATUS_Separated',
         'NAME_FAMILY_STATUS_Singlenotmarried', 'NAME_FAMILY_STATUS_Widow', 'NAME_HOUSING_TYPE_Coopapartment',
         'NAME_HOUSING_TYPE_Houseapartment', 'NAME_HOUSING_TYPE_Municipalapartment',
         'NAME_HOUSING_TYPE_Officeapartment', 'NAME_HOUSING_TYPE_Rentedapartment', 'NAME_HOUSING_TYPE_Withparents',
         'OCCUPATION_TYPE_Accountants', 'OCCUPATION_TYPE_Cleaningstaff', 'OCCUPATION_TYPE_Cookingstaff',
         'OCCUPATION_TYPE_Corestaff', 'OCCUPATION_TYPE_Drivers', 'OCCUPATION_TYPE_HRstaff',
         'OCCUPATION_TYPE_Highskilltechstaff', 'OCCUPATION_TYPE_ITstaff', 'OCCUPATION_TYPE_Laborers',
         'OCCUPATION_TYPE_LowskillLaborers', 'OCCUPATION_TYPE_Managers', 'OCCUPATION_TYPE_Medicinestaff',
         'OCCUPATION_TYPE_Other', 'OCCUPATION_TYPE_Privateservicestaff', 'OCCUPATION_TYPE_Realtyagents',
         'OCCUPATION_TYPE_Salesstaff', 'OCCUPATION_TYPE_Secretaries', 'OCCUPATION_TYPE_Securitystaff',
         'OCCUPATION_TYPE_Waitersbarmenstaff', 'ORGANIZATION_TYPE_Advertising', 'ORGANIZATION_TYPE_Agriculture',
         'ORGANIZATION_TYPE_Bank', 'ORGANIZATION_TYPE_Business', 'ORGANIZATION_TYPE_Cleaning',
         'ORGANIZATION_TYPE_Construction', 'ORGANIZATION_TYPE_Culture', 'ORGANIZATION_TYPE_Electricity',
         'ORGANIZATION_TYPE_Emergency', 'ORGANIZATION_TYPE_Government', 'ORGANIZATION_TYPE_Hotel',
         'ORGANIZATION_TYPE_Housing', 'ORGANIZATION_TYPE_Industry', 'ORGANIZATION_TYPE_Insurance',
         'ORGANIZATION_TYPE_Kindergarten', 'ORGANIZATION_TYPE_LegalServices', 'ORGANIZATION_TYPE_Medicine',
         'ORGANIZATION_TYPE_Military', 'ORGANIZATION_TYPE_Mobile', 'ORGANIZATION_TYPE_Other',
         'ORGANIZATION_TYPE_Police', 'ORGANIZATION_TYPE_Postal', 'ORGANIZATION_TYPE_Realtor',
         'ORGANIZATION_TYPE_Religion', 'ORGANIZATION_TYPE_Restaurant', 'ORGANIZATION_TYPE_School',
         'ORGANIZATION_TYPE_Security', 'ORGANIZATION_TYPE_SecurityMinistries', 'ORGANIZATION_TYPE_Selfemployed',
         'ORGANIZATION_TYPE_Services', 'ORGANIZATION_TYPE_Telecom', 'ORGANIZATION_TYPE_Trade',
         'ORGANIZATION_TYPE_Transport', 'ORGANIZATION_TYPE_University']]

    # заполнение получившихся новых ячеек нулями
    df = df.fillna(0)

    # загрузка модели
    with open("scoring_model.pkl", 'rb') as file:
         model = pickle.load(file)

    # узнаем предсказание модели
    y_predict = model.predict_proba(df)
    # выводим его на экран
    print(y_predict[:, 1])




def mapping(datajson:pd.DataFrame):
    datajson['AGE'] = ((datajson['DAYS_BIRTH']).astype('int64') / 365).astype('int64')

    datajson['OWN_CAR'] = datajson["FLAG_OWN_CAR"]

    datajson['IS_MEN'] = datajson['CODE_GENDER'].str.contains("M")
    datajson['IS_FEMALE'] = datajson['CODE_GENDER'].str.contains("F")

    datajson['EXPERIENCE'] = datajson['DAYS_EMPLOYED'].astype('int64')

    datajson['CREDIT_INCOME_PERCENT'] = (datajson['AMT_CREDIT']).astype('float') / (
    datajson['AMT_INCOME_TOTAL']).astype('float')
    datajson['ANNUITY_INCOME_PERCENT'] = (datajson['AMT_ANNUITY']).astype('float') / (
    datajson['AMT_INCOME_TOTAL']).astype('float')
    datajson['CREDIT_TERM'] = (datajson['AMT_ANNUITY']).astype('float') / (datajson['AMT_CREDIT']).astype('float')
    datajson['EXPERIENCE_PERCENT'] = datajson['EXPERIENCE'] / datajson['AGE']

    datajson['EDUCATION'] = datajson['NAME_EDUCATION_TYPE'].map(
        {'Lower secondary': 0, 'Secondary / secondary special': 1, 'Incomplete higher': 2, 'Higher education': 3,
         'Academic degree': 4})

    datajson = datajson.drop(
        ['CODE_GENDER', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'NAME_EDUCATION_TYPE', 'FLAG_OWN_CAR', 'SURNAME', 'NAME',
         'PATRONYMIC', 'PASSPORT'], axis=1)
    datajson = pd.get_dummies(datajson)
    datajson = datajson.rename(columns=lambda x: re.sub('[^A-Za-z0-9_]+', '', x))


    return datajson


if __name__ == "__main__":
    main_def() # временно
    # uvicorn.run(app, host="127.0.0.1", port=8888)