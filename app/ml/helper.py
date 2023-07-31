import re
import pandas as pd

def apply_mapping(df):
    df['AGE'] = ((df['DAYS_BIRTH']).astype('int64') / 365).astype('int64')

    df['OWN_CAR'] = df["FLAG_OWN_CAR"]

    df['IS_MEN'] = df['CODE_GENDER'].str.contains("M")
    df['IS_FEMALE'] = df['CODE_GENDER'].str.contains("F")

    df['EXPERIENCE'] = df['DAYS_EMPLOYED'].astype('int64')

    df['MONTHS_CREDIT'] = (df['AMT_ANNUITY']).astype('int64')

    df['AMT_ANNUITY'] = df['AMT_CREDIT'] / df['AMT_ANNUITY']

    df['CREDIT_INCOME_PERCENT'] = (df['AMT_CREDIT']).astype('float') / (
    df['AMT_INCOME_TOTAL']).astype('float')
    df['ANNUITY_INCOME_PERCENT'] = (df['AMT_ANNUITY']).astype('float') / (
    df['AMT_INCOME_TOTAL']).astype('float')
    df['CREDIT_TERM'] = (df['AMT_ANNUITY']).astype('float') / (df['AMT_CREDIT']).astype('float')
    df['EXPERIENCE_PERCENT'] = df['EXPERIENCE'] / df['AGE']

    df['EDUCATION'] = df['NAME_EDUCATION_TYPE'].map(
        {'Lower secondary': 0, 'Secondary / secondary special': 1, 'Incomplete higher': 2, 'Higher education': 3,
         'Academic degree': 4})

    df = df.drop(
        ['CODE_GENDER', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'NAME_EDUCATION_TYPE', 'FLAG_OWN_CAR'], axis=1)
    df = pd.get_dummies(df)
    df = df.rename(columns=lambda x: re.sub('[^A-Za-z0-9_]+', '', x))
    return df

def reorder_df(df):
    list = ['CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'MONTHS_CREDIT', 'OWN_CAR', 'IS_MEN',
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
         'ORGANIZATION_TYPE_Transport', 'ORGANIZATION_TYPE_University']
    for x in df:
        if x not in list:
            print(x)
    df = df[list]
    return df