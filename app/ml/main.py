import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from helper import apply_mapping, reorder_df

PORT = 8888

app = FastAPI()

model = joblib.load('./model/best_extra_scoring_model.sav')

class ModelData(BaseModel):
    CODE_GENDER: str
    DAYS_BIRTH: int
    NAME_FAMILY_STATUS: str
    CNT_CHILDREN: int
    NAME_HOUSING_TYPE: str
    FLAG_OWN_CAR: str
    NAME_EDUCATION_TYPE: str
    OCCUPATION_TYPE: str
    ORGANIZATION_TYPE: str
    DAYS_EMPLOYED: int
    NAME_INCOME_TYPE: str
    AMT_INCOME_TOTAL: float
    AMT_CREDIT: int
    AMT_ANNUITY: float

@app.post("/")
async def root(model_data: ModelData):
    df = pd.DataFrame([dict(model_data)])
    df = apply_mapping(df)
    pattern = pd.read_csv("app_file.csv")
    df, _ = df.align(pattern, join='outer', axis=1)
    df = reorder_df(df)
    df = df.fillna(0)
    y_predict = model.predict_proba(df)
    return y_predict[0, 1]

if __name__ == "__main__":
    uvicorn.run(app, port=PORT)