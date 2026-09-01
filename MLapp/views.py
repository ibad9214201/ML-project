
import base64
from io import BytesIO
import io

from django.http import JsonResponse
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
from django.shortcuts import HttpResponse, render
from sklearn.compose import ColumnTransformer
from sklearn.discriminant_analysis import StandardScaler
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, r2_score
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeClassifier
from MLapp.models import HousePrice

def House(request):
    data = pd.read_excel(r"C:\Users\Speed Computers\Downloads\pricehouse.xlsx")
    for i, row in data.iterrows():
        HousePrice.objects.create(
            Size_sqft=row["Size_sqft"],
            Bedrooms=row['Bedrooms'],
            Bathrooms=row['Bathrooms'],
            Age_years=row['Age_years'],
            Distance_to_city_km=row['Distance_to_city_km'],
            Location_type=row['Location_type'],
            Condition=row['Condition'],
            House_Price=row['House_Price'],
        )
    employ=HousePrice.objects.all()
    return render(request,"Houseprice.html",{"employ":employ})
def Decisiontree_load_data(request):
    data= pd.read_excel(r"C:\Users\Speed Computers\Downloads\football.xlsx")
    for index , i in data.iterrows():
        FootballMatch.objects.create(
            Weather=i['Weather'],
            Temperature=i['Temperature'],
            Humidity=i['Humidity'],
            Wind=i['Wind'],
            Weekend=i['Weekend'],
            Ground_Condition=i['Ground_Condition'],
            Play_Football=i['Play_Football']
        )
    return render(request,"mainml.html",)
def Decisiontree(request):
    data=FootballMatch.objects.all().order_by('id').values()
    df=pd.DataFrame(list(data))
    x=df[['Weather','Temperature','Humidity','Wind','Weekend','Ground_Condition']]
   # df['Play_Football'] = df['Play_Football'].str.strip().str.capitalize()
    y=df['Play_Football'].map({'Yes':1,"No":0})
    
    categorical =['Weather','Temperature','Humidity','Wind','Weekend','Ground_Condition']
    process = ColumnTransformer(transformers=[
    ("encoded", OneHotEncoder(handle_unknown='ignore'), categorical)])
    pipe=Pipeline(steps=[
        ('process',process),('Decision', DecisionTreeClassifier(max_depth=1,random_state=42))
    ])
    x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42,test_size=0.2)
    pipe.fit(x_train,y_train)
    predict=pipe.predict(x_test)
    print(predict)
    cm=confusion_matrix(y_test,predict)
    accuracy=accuracy_score(y_test,predict)
    precision=precision_score(y_test,predict)
    recall=recall_score(y_test,predict)
    f1=f1_score(y_test,predict)
    report=classification_report(y_test,predict,output_dict=True)
 
    context={
        'predictions': list(predict),
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'report': report,
       # 'cm_image': image_base64,
        'x_test': x_test.to_dict(orient='records')

    }
    weather=FootballMatch.objects.values_list("Weather",flat=True).distinct()
    temperature = FootballMatch.objects.values_list("Temperature", flat=True).distinct()
    humidity = FootballMatch.objects.values_list("Humidity", flat=True).distinct()
    wind = FootballMatch.objects.values_list("Wind", flat=True).distinct()
    weekend = FootballMatch.objects.values_list("Weekend", flat=True).distinct()
    ground = FootballMatch.objects.values_list("Ground_Condition", flat=True).distinct()
    context = {
    "weather": weather,
    "temperature": temperature,
    "humidity": humidity,
    "wind": wind,
    "weekend": weekend,
    "ground": ground,
    "accuracy":accuracy,
    "Precision":precision,
    'recall':recall,
    "f1":f1,
    "report":report}
    if request.method=="POST":
        action=request.POST.get("hidden_value")
        print(action,"this is predict input")
        if action=="predict":
            Decision={
            "Weather":request.POST.get("weather"),
            "Temperature":request.POST.get("temperature"),
            "Humidity":request.POST.get("humidity"),
            "Wind":request.POST.get("wind"),
            "Weekend":request.POST.get("Weakend"),
            "Ground_Condition":request.POST.get("Ground_Condition"),
        }
            print(Decision['Weather'])
            
            dp=pd.DataFrame([Decision])
            prediction=pipe.predict(dp)
            print(prediction,"THESSSSSSSSSSSSSSS")
            if prediction[0]==1:
                return JsonResponse({'Success':True,"predict":"Yes"})
            else:
                return JsonResponse({'Success':True,"predict":"NO"})
        elif action=="max_depth":
            depth={
            "Start":request.POST.get('Start'),
            "End":request.POST.get('End'),
        }
            max_depth=range(int(depth["Start"]),int(depth["End"]))
            print(max_depth,"ssssss")
            score=[]
            for k in max_depth:
                pipe=Pipeline(steps=[('process',process),('Decision',DecisionTreeClassifier(max_depth=k))])
                cv_score=cross_val_score(pipe,x,y ,scoring="accuracy", ).mean()
                print("Hello",cv_score)
                score.append(cv_score)
           
            best_index = score.index(max(score))
            best_depth = list(max_depth)[best_index]
            
            return JsonResponse({"Success":True,"depth":best_depth})
            print(score)
          #  for d , s in zip(best_depth):
           #     print(d +"and " +s,"score")
    
        
        
    

    return render(request,"Decision.html",context)
def Depth(request):
    if request.method=="POST":
        depth={
            "Start":request.POST.get('Start'),
            "End":request.POST.get('End'),
        }
        start=int(depth["Start"])
        end=int(depth['End'])
        max_depth=range(start,end)
        score=[]
        for k in max_depth:
            pipe=Pipeline(steps=['Decision',DecisionTreeClassifier(max_depth=k)])
           # cv_score=cross_val_score(pip,x,y ,scoring="accuracy", ).mean()
            #score.append(cv_score)

            


def mainhtml(request):
    return render(request,"mainml.html")
def House_price(request):
    if request.method=="POST":
        employe={
            'Size_sqft':request.POST.get('Size_sqft'),
            'Bedrooms':request.POST.get('Bedrooms'),
            'Bathrooms':request.POST.get('Bathrooms'),
            'Age_years':request.POST.get('Age_years'),
            'Distance_to_city_km':request.POST.get('Distance_to_city_km'),
            'Location_type':request.POST.get('Location_type'),
            'Condition':request.POST.get('Condition'),
            'House_Price':request.POST.get('House_Price')
        }
        HousePrice.objects.create(**employe)
        house=HousePrice.objects.all().values()
        df=pd.DataFrame(list(house))
        df = df.astype({
            'Size_sqft': float,
            'Bedrooms': int,
            'Bathrooms': int,
            'Distance_to_city_km': float,
            'House_Price': float
        })
        x=df[["Size_sqft","Bedrooms","Bathrooms","Distance_to_city_km"]]
        y=df["House_Price"]
        transf=ColumnTransformer(
        transformers=[
            ("scaler",StandardScaler(),["Size_sqft","Bedrooms","Bathrooms","Distance_to_city_km"])
        ]
    )
        pip=Pipeline(steps=[
         ('transf',transf),
        ('linear',LinearRegression())
    ])
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2, random_state=42)
        pip.fit(x_train,y_train)
        y_pred=pip.predict(x_test)
        error=y_test-y_pred
        mse=np.mean(error**2)
        rmse=np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
      #  slope=pip.named_steps['linear'].coef_
        intercept=pip.named_steps['linear'].intercept_
        feature_name=pip.named_steps['transf'].get_feature_names_out()
        slope=pip.named_steps['linear'].coef_
        for name , coeff in zip(feature_name,slope):
            print(name,coeff)
        predicted = {
            "y_pred": y_pred.tolist(),
            "error": error.tolist(),
            "mse": mse,
            "rmse": rmse,
            "r2": r2,
            "intercept":intercept,
        }
        print(predicted,'this your predicate score ')

        return JsonResponse({"sucess":True,"predicted":predicted})
    employ=HousePrice.objects.all()
    return render(request,"Houseprice.html",{"employ":employ})
def predictvalue(request):
    if request.method=="POST":
        house=HousePrice.objects.all().values()
        df=pd.DataFrame(list(house))
        x=df[["Size_sqft","Bedrooms","Bathrooms","Distance_to_city_km"]]
        y=df["House_Price"]
        transf=ColumnTransformer(
        transformers=[
            ("scaler",StandardScaler(),["Size_sqft","Bedrooms","Bathrooms","Distance_to_city_km"])
        ])
        pip=Pipeline(steps=[
         ('transf',transf),
        ('linear',LinearRegression())])
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2, random_state=42)
        pip.fit(x_train,y_train)
        y_pred=pip.predict(x_test)
        error=y_test-y_pred
        mse=np.mean(error**2)
        rmse=np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
      #  slope=pip.named_steps['linear'].coef_
        intercept=pip.named_steps['linear'].intercept_
        feature_name=pip.named_steps['transf'].get_feature_names_out() 
        predict_value={
            'Size_sqft':request.POST.get('Size_sqft'),
            'Bedrooms':request.POST.get('Bedrooms'),
            'Bathrooms':request.POST.get('Bathrooms'),
            'Distance_to_city_km':request.POST.get('Distance_to_city_km'),
        }
        dp=pd.DataFrame([predict_value])
        predication=pip.predict(dp)
        print(predication)
        predicted = {
            "y_pred": predication.tolist(),
            "error": error.tolist(),
            "mse": mse,
            "rmse": rmse,
            "r2": r2,
            "intercept":intercept,
        }
        print(predicted,'this your predicate score ')
        return JsonResponse({"sucess":True,"predicted":predicted})
    return HttpResponse("predict")
def delete_employee(request):
    if request.method=="POST":
        del_id = request.POST.get("id")
        print(del_id)
        if not del_id:
            return JsonResponse({
                "success":False,
                "error": "Missing employe id"
            }, status=400) 
        house=HousePrice.objects.get(id=del_id)
        house.delete()
        return JsonResponse({
            "success":True,
            "message":f"record {del_id} deleted succesufuly "
        })
    return HttpResponse("del")
from .models import FootballMatch, Footballclassification, HousePrice

def Edit_Data(request):
    if request.method == "POST":

        upd = request.POST.get("id")

        house = HousePrice.objects.get(id=upd)

        data = {
            "id":house.id,
            "Size_sqft": house.Size_sqft,
            "Bedrooms": house.Bedrooms,
            "Bathrooms": house.Bathrooms,
            "Age_years": house.Age_years,
            "Distance_to_city_km": house.Distance_to_city_km,
            "Location_type": house.Location_type,
            "Condition": house.Condition,
            "House_Price": house.House_Price
        }
        print(data)

        return JsonResponse(data)
def update_Data(request):
    if request.method=="POST":
        id=int(request.POST.get('id'))
        updata={
            
            'Size_sqft':request.POST.get('Size_sqft'),
            'Bedrooms':request.POST.get('Bedrooms'),
            'Bathrooms':request.POST.get('Bathrooms'),
            'Age_years':request.POST.get('Age_years'),
            'Distance_to_city_km':request.POST.get('Distance_to_city_km'),
            'Location_type':request.POST.get('Location_type'),
            'Condition':request.POST.get('Condition'),
            'House_Price':request.POST.get('House_Price')
        }
        HousePrice.objects.filter(id=id).update(
           Size_sqft=updata['Size_sqft'],
           Bedrooms=updata['Bedrooms'],
           Bathrooms=updata["Bathrooms"],
           Age_years=updata["Age_years"],
           Distance_to_city_km=updata['Distance_to_city_km'],
           Location_type=updata["Location_type"],
           Condition=updata["Condition"],
           House_Price=updata['House_Price'] 
       )
        return JsonResponse({ "status":"success", "message":"Data Succesfully update"})
        
    return HttpResponse("hello")
#the next part Poly nomail regression 
def poly_nomial(request):
    if request.method=="POST":
        poly={
            "Size_sqft":request.POST.get('Size_sqft'),
            "Bedrooms":request.POST.get('Bedrooms'),
            "Bathrooms":request.POST.get('Bathrooms'),
            "Age_years":request.POST.get('Age_years'),
            "Distance_to_city_km":request.POST.get('Distance_to_city_km'),
            "Location_type":request.POST.get('Location_type'),
            "Condition":request.POST.get('Condition'),
            "House_Price":request.POST.get('House_Price'),
        }
        print(poly)
        HousePrice.objects.create(**poly)
        return JsonResponse({'status':"success"})
    house=HousePrice.objects.all()
    return render(request,"poly.html",{'house':house})
def poly_predict(request):
    if request.method=="POST":
        poly=HousePrice.objects.all().values()
        df=pd.DataFrame(list(poly))
        x=df[["Size_sqft","Bedrooms","Bathrooms","Distance_to_city_km"]]
        y=df["House_Price"]
        transfer=ColumnTransformer(transformers=[
            ('scale','passthrough',["Size_sqft","Bedrooms","Bathrooms","Distance_to_city_km"])
        ])
        pipe=Pipeline(steps=[('transf',transfer),
            ('polynomial',PolynomialFeatures(degree=2,include_bias=False)),
                             ('scale',StandardScaler()),
                             ('linear',LinearRegression()),
                             ])
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42,shuffle=True)
        pipe.fit(x_train,y_train)
        pred=pipe.predict(x_test)
        error=y_test-pred
        mse=np.mean(error**2)
        rmse=np.sqrt(mse)
        r2=r2_score(y_test,pred)
        slope=pipe.named_steps['linear'].coef_
        intercept=pipe.named_steps['linear'].intercept_
        employes={
            'Size_sqft':float(request.POST.get('Size_sqft')),
            'Bedrooms':float(request.POST.get('Bedrooms')),
            'Bathrooms':float(request.POST.get('Bathrooms')),
            'Distance_to_city_km':float(request.POST.get('Distance_to_city_km'))
        }
        dp=pd.DataFrame([employes])
        y_pred=pipe.predict(dp)
        plt.figure(figsize=(3,4))
        plt.scatter(x_test["Bedrooms"],y_test,color="green", label="Actual Data")
        plt.scatter(x_test["Bedrooms"],pred,color="green", label="Actual Data")
        x_lin=np.linspace(x['Bedrooms'].min(),x["Bedrooms"].max(),50)
        mean_value={
            'Bathrooms':x["Bathrooms"].mean(),
            'Size_sqft':x["Size_sqft"].mean(),
            'Distance_to_city_km':x["Distance_to_city_km"].mean(),
        }
        pred_dp=pd.DataFrame({
            'Size_sqft':mean_value["Size_sqft"],
            'Bedrooms':x_lin,
            'Bathrooms':mean_value["Bathrooms"],
            "Distance_to_city_km":mean_value['Distance_to_city_km']
            })
        p_predict=pipe.predict(pred_dp)
       # plt.plot(x_lin,p_predict, color="blue", label="Polynomial Fit")
       # plt.xlabel("Bedrooms Value")
       # plt.ylabel("predict vale")
       # plt.legend()
       # plt.tight_layout()
        
        
      #  buffer=BytesIO()
      #  plt.savefig(buffer,format='png')
      #  plt.close()
      #  buffer.seek(0)
      #  image_png=buffer.getvalue()
      #  graph=base64.b64encode(image_png).decode('utf-8')
      #  buffer.close(),
        #second graph 3d dimension graph
      #  fig=plt.figure(figsize=(3,4))
      #  ax=fig.add_subplot(111,projection="3d")
      #  sc=ax.scatter(df['Size_sqft'],df['Distance_to_city_km'],df['House_Price'],c=df['Bedrooms'],cmap="coolwarm",edgecolor='black',linewidth=0.9,marker='o', label='HouseData')
      #  plt.colorbar(sc,label='Age',shrink=0.5),
      #  ax.set_xlabel("Size of",fontsize=12,fontweight='bold')
      #  ax.set_ylabel("Distance",fontsize=12,fontweight='bold')
      #  ax.set_zlabel("House price",fontsize=12,fontweight='bold',)
      #  ax.set_title("3D House price graph")
      #  ax.legend("House price")
      #  plt.tight_layout()
        
     #   bufer=BytesIO()
     #   plt.savefig(bufer,format='png')
     #   plt.close(fig)
     #   bufer.seek(0)
      #  image=bufer.getvalue()
      #  graph2=base64.b64encode(image).decode('utf-8')
        
      #  bufer.close()
        context={
    #'graph':graph,
    #'graph2':graph2,
    'predication':y_pred.tolist(),
    'mse':float(mse),
    'rmse':float(rmse),
    'error':float(np.mean(np.abs(error))),
    'r2':float(r2),
    'slope':slope.tolist(),
    'intercept':float(intercept)
}
    else:   
        return JsonResponse({"success":True,"predict":context})
    #return render(request,"poly.html",{'graph':graph,"graph":graph2})
    
def GradientBoosting(request):
    house=HousePrice.objects.all().order_by('id').values()
    df=pd.DataFrame(list(house))
    x=df[['Size_sqft','Bedrooms','Bathrooms','Distance_to_city_km']]
    y=df['House_Price']
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
    Col = ColumnTransformer([('scaler', StandardScaler(), ['Size_sqft', 'Bedrooms', 'Bathrooms', 'Distance_to_city_km'])])
    pipe = Pipeline(steps=[('col',Col),
        ('scaler', StandardScaler()),
                           ('boosting', GradientBoostingRegressor(n_estimators=20, learning_rate=0.1, max_depth=3, random_state=42))])
    pipe.fit(x_train, y_train)
    y_pred = pipe.predict(x_test)
    error = y_test - y_pred
    mse = np.mean(error ** 2)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    cross=cross_val_score(pipe,x,y,cv=5,scoring="r2").mean()
    mae = mean_absolute_error(y_test, y_pred)
    if request.method=="POST":
        predict_value={
            'Size_sqft':float(request.POST.get('size')),
            'Bedrooms':int(request.POST.get('bedrooms')),
            'Bathrooms':int(request.POST.get('bathrooms')),
        #    'age':int(request.POST.get('age')),
            'Distance_to_city_km':float(request.POST.get('distance'))
        }
        print("showe", predict_value)
        dp=pd.DataFrame([predict_value])
        y_pred=pipe.predict(dp)
        print("y_pred",y_pred)
        return JsonResponse({"success":True,"predicted":float(y_pred[0])})
    return render(request,"gradientboosting.html",{'house':df,'mse':mse,'rmse':rmse,'r2':r2,'cross':cross,'mae':mae})

def Gradientclass_load(request):
    data= pd.read_excel(r"C:\Users\Speed Computers\Downloads\football_dataset.xlsx")
    print(data.head(3))
    for index , i in data.iterrows():
        Footballclassification.objects.create(
            Weather=i['Weather'],
            Temperature=i['Temperature'],
            Humidity=i['Humidity'],
            Wind=i['Wind'],
            Weekend=i['Weekend'],
            Ground_Condition=i['Ground_Condition'],
            Time_of_Day=i['Time_of_Day'],
            Play_Football=i['Play_Football']
        )
    return render(request, "gradientclass.html")

def Gradientclass(request):
    data = Footballclassification.objects.all().order_by('id').values()
    df = pd.DataFrame(list(data))
    x = df[['Weather', 'Temperature', 'Humidity', 'Wind', 'Weekend', 'Ground_Condition', 'Time_of_Day']]
    y = df['Play_Football'].map({'Yes': 1, "No": 0})

    categorical = ['Weather', 'Temperature', 'Humidity', 'Wind', 'Weekend', 'Ground_Condition', 'Time_of_Day']
    process = ColumnTransformer(transformers=[
        ("encoded", OneHotEncoder(handle_unknown='ignore'), categorical)])
    pipe = Pipeline(steps=[
        ('process', process), ('GradientBoosting', GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42))
    ])
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=0.2)
    pipe.fit(x_train, y_train)
    predict = pipe.predict(x_test)
    print(predict)
    accuracy = accuracy_score(y_test, predict.round())
    precision = precision_score(y_test, predict.round())
    recall = recall_score(y_test, predict.round())
    f1 = f1_score(y_test, predict.round())
    report = classification_report(y_test, predict.round(), output_dict=True)
    print(precision, recall, f1, report)
    print(report['1']['precision'], report['1']['recall'], report['1']['f1-score'])
    return render(request, "gradientclass.html", )

