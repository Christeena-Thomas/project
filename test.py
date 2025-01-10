import joblib
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import pandas as pd




model = joblib.load('./model_campus_placemen')
new_data = pd.DataFrame({
    'CGPA':6.3,
    'Number of MOOC Courses':2,
    'Number of Internships':0
},index=[0])

print(model.predict(new_data))
probabilities = model.predict_proba(new_data)[0]
print(probabilities)

