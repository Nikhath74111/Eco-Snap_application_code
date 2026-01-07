# Importing essential libraries and modules

from flask import Flask, render_template, request, Markup
import numpy as np
#import pandas as pd
import os
import requests 
import config
import pickle
import io
from PIL import Image 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd 
# ==============================================================================================
# ==============================================================================================
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

gmail_list=[]
password_list=[]
gmail_list1=[]
password_list1=[]
# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

# Load the dataset
#df = pd.read_csv('balanced_seizure_dataset_with_ids.csv')

# Drop unnamed index column if present
#df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Load the trained model
#with open("rf_model.pkl", "rb") as file:
#    loaded_model = pickle.load(file)



#disease_dic= ["Eye Spot","Healthy Leaf","Red Leaf Spot","Redrot","Ring Spot"]



from model_predict2  import pred_waste_type



# ===============================================================================================
# ------------------------------------ FLASK APP -------------------------------------------------


app = Flask(__name__)

# render home page



#@ app.route('/')
#def home():
#    title = 'Multiple cancer Identification using Deeplearning'
#    return render_template('index.html', title=title)  
@app.route('/')
def home():
    return render_template('home1.html')        


 

@app.route('/patient',methods=['POST',"GET"])
def patient():
    return render_template('login44.html')    


@app.route('/admin',methods=['POST',"GET"])
def admin():
    return render_template('login442.html') 

@app.route('/register22',methods=['POST',"GET"])
def register22():
    return render_template('register442.html') 

@app.route('/register2',methods=['POST',"GET"])
def register2():
    return render_template('register44.html')  
import pickle
@app.route('/logedin',methods=['POST'])
def logedin():
    
    int_features3 = [str(x) for x in request.form.values()]
    print(int_features3)
    logu=int_features3[0]
    passw=int_features3[1]
    

    name =int_features3[0]

    # Save to a file
    with open("name.pkl", "wb") as f:
        pickle.dump(name, f)

   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root","","ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
              #print(result1)
              #print(gmail1)
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list.append(str(row1[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(gmail_list)
    

    cursor1= db.cursor()
    cursor1.execute("SELECT password FROM user_register")
    result2=cursor1.fetchall()
              #print(result1)
              #print(gmail1)
    for row2 in result2:
                      print(row2)
                      print(row2[0])
                      password_list.append(str(row2[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(password_list)
    print(gmail_list.index(logu))
    print(password_list.index(passw))
    
    if gmail_list.index(logu)==password_list.index(passw):
        return render_template('index.html')
    else:
        return jsonify({'result':'use proper  gmail and password'})
                  
                                               


@app.route('/logedin2',methods=['POST'])
def logedin2():
    
    int_features3 = [str(x) for x in request.form.values()]
    print(int_features3)
    logu=int_features3[0]
    passw=int_features3[1]
   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root","","ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
              #print(result1)
              #print(gmail1)
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list.append(str(row1[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(gmail_list)
    

    cursor1= db.cursor()
    cursor1.execute("SELECT password FROM user_register")
    result2=cursor1.fetchall()
              #print(result1)
              #print(gmail1)
    for row2 in result2:
                      print(row2)
                      print(row2[0])
                      password_list.append(str(row2[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(password_list)
    print(gmail_list.index(logu))
    print(password_list.index(passw))
    
    if gmail_list.index(logu)==password_list.index(passw):
        return render_template('patient_info.html')
    else:
        return jsonify({'result':'use proper  gmail and password'})
                  
                                               

import pandas as pd
from flask import request, render_template



@app.route('/get-patient-info', methods=['GET', 'POST'])
def get_waste_info():
    if request.method == 'POST':
        user_id = request.form.get('user_id')  # Changed from patient_id to user_id
        try:
            waste_csv = 'waste_data.csv'
            
            if not os.path.exists(waste_csv):
                return render_template('patient_info.html', error="No waste data available.", waste_records=[])

            # Load waste data
            waste_df = pd.read_csv(waste_csv)
            
            # Filter records for the given user_id
            user_waste_records = waste_df[waste_df['user_id'] == user_id]
            
            if user_waste_records.empty:
                return render_template('patient_info.html', 
                                     message=f"No waste records found for user ID: {user_id}", 
                                     waste_records=[])

            # Convert to list of dictionaries
            waste_list = user_waste_records.to_dict('records')

            print(waste_list)

            # Clean up disposal_locations: split semicolon-separated string into list
            for record in waste_list:
                if 'disposal_locations' in record and pd.notna(record['disposal_locations']):
                    locations = record['disposal_locations']
                    if isinstance(locations, str):
                        record['disposal_locations'] = [
                            loc.strip() for loc in locations.split(';') if loc.strip()
                        ]
                    else:
                        record['disposal_locations'] = []
                else:
                    record['disposal_locations'] = []

            return render_template(
                'patient_info.html',
                waste_records=waste_list,
                user_id=user_id
            )

        except Exception as e:
            return render_template('patient_info.html', error=f"Error: {str(e)}", waste_records=[])

    # GET request: show form
    return render_template('patient_info.html')
    

              
              # int_features3[0]==12345 and int_features3[1]==12345:
               #                      return render_template('index.html')
        
@app.route('/register',methods=['POST'])
def register():
    

    int_features2 = [str(x) for x in request.form.values()]
    #print(int_features2)
    #print(int_features2[0])
    #print(int_features2[1])
    r1=int_features2[0]
    print(r1)
    
    r2=int_features2[1]
    print(r2)
    logu1=int_features2[0]
    passw1=int_features2[1]
        
    

    

   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root",'',"ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
              #print(result1)
              #print(gmail1)
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list1.append(str(row1[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(gmail_list1)
    if logu1 in gmail_list1:
                      return jsonify({'result':'this gmail is already in use '})  
    else:

                  #return jsonify({'result':'this  gmail is not registered'})
              

# Prepare SQL query to INSERT a record into the database.
                  sql = "INSERT INTO user_register(user,password) VALUES (%s,%s)"
                  val = (r1, r2)
   
                  try:
   # Execute the SQL command
                                       cursor.execute(sql,val)
   # Commit your changes in the database
                                       db.commit()
                  except:
   # Rollback in case there is any error
                                       db.rollback()

# disconnect from server
                  db.close()
                 # return jsonify({'result':'succesfully registered'})
                  return render_template('login44.html')

@app.route('/register24',methods=['POST'])
def register24():
    

    int_features2 = [str(x) for x in request.form.values()]
    #print(int_features2)
    #print(int_features2[0])
    #print(int_features2[1])
    r1=int_features2[0]
    print(r1)
    
    r2=int_features2[1]
    print(r2)
    logu1=int_features2[0]
    passw1=int_features2[1]
        
    

    

   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root",'',"ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
              #print(result1)
              #print(gmail1)
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list1.append(str(row1[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(gmail_list1)
    if logu1 in gmail_list1:
                      return jsonify({'result':'this gmail is already in use '})  
    else:

                  #return jsonify({'result':'this  gmail is not registered'})
              

# Prepare SQL query to INSERT a record into the database.
                  sql = "INSERT INTO user_register(user,password) VALUES (%s,%s)"
                  val = (r1, r2)
   
                  try:
   # Execute the SQL command
                                       cursor.execute(sql,val)
   # Commit your changes in the database
                                       db.commit()
                  except:
   # Rollback in case there is any error
                                       db.rollback()

# disconnect from server
                  db.close()
                 # return jsonify({'result':'succesfully registered'})
                  return render_template('login442.html')                      
# render crop recommendation form page

from flask import request, render_template
from PIL import Image
import os
import pandas as pd
from datetime import datetime



@app.route('/waste-predict', methods=['GET', 'POST'])
def waste_prediction():
    title = 'Waste Type Identification & Recycling Information System'

    if request.method == 'POST':
        file = request.files.get('file')

        # Load user/product ID (replace with your own stored pickle)
        with open("name.pkl", "rb") as f:
            user_id = pickle.load(f)

        print("User ID:", user_id)
        if not file or not user_id:
            return render_template('rust.html', title=title)

        # Save uploaded image
        img = Image.open(file)
        img.save('waste_output.png')

        # --- Call your model prediction function ---
        prediction, confidence = pred_waste_type("waste_output.png")  # <-- Your model function
        print("Predicted Waste Type:", prediction)
 
        if prediction.lower() == "unknown":
            return render_template('error_page.html')

        # --- Waste Information Database ---
        waste_info = {
            "E-waste": {
                "description": "Electronic waste like old phones, laptops, and circuit boards.",
                "disposal_method": "Send to certified e-waste recycling centers.",
                "recyclable": "Yes, about 90% components can be recovered.",
                "energy_used": "Consumes around 1.5 kWh per kg in recycling.",
                "water_usage": "Minimal water used in dismantling; chemical recycling uses ~10L/kg.",
                "hazards": "Contains lead, mercury, and cadmium which are toxic if untreated.",
                "recycling_benefit": "Recovers precious metals like gold, silver, and copper.",
                "co2_saving": "Recycling 1 ton saves ~1.5 tons CO₂ emissions.",
                "disposal_locations": [
                   "https://maps.google.com/?q=E-waste+Recycling+Center+Bangalore",
                    "https://maps.google.com/?q=E-waste+Disposal+Bangalore",
                    "https://maps.google.com/?q=E-waste+Drop+Point+Bangalore"
                    
                ]
            },
            "automobile wastes": {
                "description": "Scrap parts, oils, and batteries from vehicles.",
                "disposal_method": "Hand over to authorized automobile scrap dealers.",
                "recyclable": "Yes, ~75% of materials are recyclable.",
                "energy_used": "Around 2 kWh/kg for metal recovery and processing.",
                "water_usage": "~5L/kg during washing and material separation.",
                "hazards": "Toxic oil residues and lead acid from batteries.",
                "recycling_benefit": "Reuses metals, rubber, and plastics reducing landfill load.",
                "co2_saving": "Saves ~1.2 tons CO₂ per ton recycled.",
                "disposal_locations": [
                    "https://maps.google.com/?q=Automobile+Scrap+Yard+Bangalore",
                    "https://maps.google.com/?q=Auto+Recycle+Bangalore",
                    "https://maps.google.com/?q=Vehicle+Disposal+Bangalore"
                ]
            },
            "battery waste": {
                "description": "Used dry cells, lithium-ion, and lead-acid batteries.",
                "disposal_method": "Submit to battery recycling collection centers.",
                "recyclable": "Yes, up to 80% recoverable materials.",
                "energy_used": "1.2 kWh/kg due to chemical processing.",
                "water_usage": "~8L/kg for electrolyte neutralization.",
                "hazards": "Contains acid and heavy metals harmful to soil and water.",
                "recycling_benefit": "Recovers lithium, nickel, and zinc for reuse.",
                "co2_saving": "Recycling 1 ton saves 0.8 tons CO₂.",
                "disposal_locations": [
                     "https://maps.google.com/?q=Battery+Recycling+Bangalore",
                    "https://maps.google.com/?q=Battery+Collection+Center+Bangalore",
                    "https://maps.google.com/?q=Battery+Drop+Point+Bangalore"

                ]
            },
            "glass waste": {
                "description": "Bottles, windows, and other glass products.",
                "disposal_method": "Segregate by color and send to glass recycling units.",
                "recyclable": "100% recyclable with no loss in quality.",
                "energy_used": "0.7 kWh/kg to melt and reshape glass.",
                "water_usage": "~2L/kg for cleaning and cooling.",
                "hazards": "Non-toxic but can cause injury if mishandled.",
                "recycling_benefit": "Saves raw materials like sand and limestone.",
                "co2_saving": "Saves ~315 kg CO₂ per ton recycled.",
                "disposal_locations": [
                       
                       "https://maps.google.com/?q=+Recycling+Plant+Bangalore"
                    "Ewaste Hub  bengaluru karnataka","Saahas Waste Management Pvt Ltd bengaluru"
                ]
            },
            "light bulbs": {
                "description": "Fluorescent and LED bulbs.",
                "disposal_method": "Drop at lighting waste collection points.",
                "recyclable": "Yes, but requires careful handling for mercury lamps.",
                "energy_used": "0.5 kWh/unit for dismantling and separation.",
                "water_usage": "Negligible.",
                "hazards": "Mercury vapor in CFLs is toxic if broken.",
                "recycling_benefit": "Glass, metal, and plastic parts reused; mercury safely recovered.",
                "co2_saving": "Saves ~120 kg CO₂ per 1000 bulbs recycled.",
                "disposal_locations": [
                   "https://maps.google.com/?q=Light+Bulb+Recycling+Bangalore",
                    "https://maps.google.com/?q=Lighting+Disposal+Bangalore",
                    "https://maps.google.com/?q=CFL+Recycle+Bangalore"
                ]
            },
            "metal waste": {
                "description": "Iron, steel, aluminum scraps from industries or households.",
                "disposal_method": "Send to authorized metal scrap recyclers.",
                "recyclable": "100% recyclable.",
                "energy_used": "Recycling uses 75% less energy than producing new metal.",
                "water_usage": "~3L/kg in cooling and cleaning.",
                "hazards": "Rust and sharp edges pose safety risks.",
                "recycling_benefit": "Preserves natural ores and reduces mining.",
                "co2_saving": "Recycling 1 ton saves ~1.4 tons CO₂.",
                "disposal_locations": [
                     "https://maps.google.com/?q=Metal+Scrap+Yard+Bangalore",
                    "https://maps.google.com/?q=Metal+Recycling+Plant+Bangalore",
                    "https://maps.google.com/?q=Steel+Recycle+Center+Bangalore"
                ]

            },
            "organic waste": {
                "description": "Kitchen waste, food residues, and biodegradable matter.",
                "disposal_method": "Composting or biogas conversion.",
                "recyclable": "Fully recyclable through natural decomposition.",
                "energy_used": "Produces energy instead (biogas).",
                "water_usage": "~1L/kg during composting.",
                "hazards": "Can produce methane if landfilled.",
                "recycling_benefit": "Converts waste into compost and clean energy.",
                "co2_saving": "Reduces greenhouse gas by ~2 tons CO₂ per ton composted.",
                "disposal_locations": [
                     "https://maps.google.com/?q=Organic+Compost+Center+Bangalore",
                    "https://maps.google.com/?q=Food+Waste+Recycling+Bangalore",
                    "https://maps.google.com/?q=Biogas+Plant+Bangalore"

                ]
            },
            "paper waste": {
                "description": "Used papers, books, and cardboard.",
                "disposal_method": "Send to paper recycling mills or collection drives.",
                "recyclable": "Yes, up to 7 times before fiber degradation.",
                "energy_used": "Recycling uses 40% less energy than virgin paper production.",
                "water_usage": "Recycling uses 50% less water (~5L/kg).",
                "hazards": "Minimal environmental risk.",
                "recycling_benefit": "Saves trees, water, and landfill space.",
                "co2_saving": "Saves ~900 kg CO₂ per ton recycled.",
                "disposal_locations": [
                     "https://maps.google.com/?q=Paper+Recycling+Plant+Bangalore",
                    "https://maps.google.com/?q=Paper+Waste+Collection+Bangalore",
                    "https://maps.google.com/?q=Paper+Recycle+Bangalore"

                ]
            },
            "plastic waste": {
                "description": "PET bottles, wrappers, and containers.",
                "disposal_method": "Clean and segregate before sending to plastic recycling units.",
                "recyclable": "Partially recyclable depending on plastic type (1–7 codes).",
                "energy_used": "~2.5 kWh/kg for melting and reshaping.",
                "water_usage": "~6L/kg for cleaning and cooling.",
                "hazards": "Releases microplastics and toxins if burned or landfilled.",
                "recycling_benefit": "Reduces petroleum use and plastic pollution.",
                "co2_saving": "Saves ~1 ton CO₂ per ton recycled.",
                "disposal_locations": [
                     "https://maps.google.com/?q=Plastic+Recycling+Plant+Bangalore",
                
                    "https://maps.google.com/?q=Plastic+Waste+Collection+Bangalore"

                ]
            }
        }

        # --- Extract Details ---
        pred_type = prediction.lower().strip()
        details = waste_info.get(pred_type, {})

        description = details.get("description", "Information not available.")
        disposal_method = details.get("disposal_method", "Information not available.")
        recyclable = details.get("recyclable", "Information not available.")
        energy_used = details.get("energy_used", "N/A")
        water_usage = details.get("water_usage", "N/A")
        hazards = details.get("hazards", "N/A")
        recycling_benefit = details.get("recycling_benefit", "N/A")
        co2_saving = details.get("co2_saving", "N/A")
        disposal_locations = details.get("disposal_locations", [])
        from gtts import gTTS
        from pydub import AudioSegment
        import pygame
        import os

        text = str(details)
        language = 'en'


        # Create gTTS object
        tts = gTTS(text=text, lang=language, slow=False)

        # Save the converted audio in a file
        tts.save("output.mp3")
        print("Audio file saved successfully.")
    
        pygame.mixer.init()

        # Load the audio file
        pygame.mixer.music.load("output.mp3")

        # Play the audio file
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Adjust the tick value as needed

        # Close the mixer
        pygame.mixer.quit()
        # --- Save to CSV (Database) ---
        csv_file = 'waste_data.csv'
        columns = [
            'user_id', 'waste_type', 'date', 'description', 'disposal_method',
            'recyclable', 'energy_used', 'water_usage', 'hazards',
            'recycling_benefit', 'co2_saving', 'disposal_locations'
        ]

        if not os.path.exists(csv_file):
            df = pd.DataFrame(columns=columns)
        else:
            df = pd.read_csv(csv_file)

        current_date = datetime.now().strftime("%Y-%m-%d")

        new_data = {
            'user_id': user_id,
            'waste_type': pred_type,
            'date': current_date,
            'description': description,
            'disposal_method': disposal_method,
            'recyclable': recyclable,
            'energy_used': energy_used,
            'water_usage': water_usage,
            'hazards': hazards,
            'recycling_benefit': recycling_benefit,
            'co2_saving': co2_saving,
            'disposal_locations': "; ".join(disposal_locations)
        }

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(csv_file, index=False)

        # --- Render Result Page ---
        return render_template(
            'rust-result.html',
            prediction=prediction.capitalize(),
            description=description,
            disposal_method=disposal_method,
            recyclable=recyclable,
            energy_used=energy_used,
            water_usage=water_usage,
            hazards=hazards,
            recycling_benefit=recycling_benefit,
            co2_saving=co2_saving,
            disposal_locations=disposal_locations,
            title="Waste Identification Result"
        )

    return render_template('rust.html', title=title)






@app.route('/waste_prediction2', methods=['GET', 'POST'])
def waste_prediction2():
    title = 'Waste Type Identification and Recycling Insights'

    if request.method == 'POST':
        file = None

        # 1️⃣ Handle camera capture (base64 image) or file upload
        if 'captured_image' in request.form and request.form['captured_image']:
            import base64
            image_data = request.form['captured_image'].split(',')[1]
            image_bytes = base64.b64decode(image_data)
            with open("output.png", "wb") as f:
                f.write(image_bytes)
            file = 'output.png'
        elif 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file:
                img = Image.open(uploaded_file)
                img.save('output.png')
                file = 'output.png'

        # 2️⃣ Load user ID (same logic as before)
        with open("name.pkl", "rb") as f:
            user_id = pickle.load(f)
        print("User ID:", user_id)

        if not file or not user_id:
            return render_template('rust2.html', title=title)

        # 3️⃣ Predict using your waste classification models
        
        

       # if prediction2 == "unknown":
       #     return render_template('error_page.html')

       
        # --- Call your model prediction function ---
        prediction, confidence = pred_waste_type("output.png")  # <-- Your model function
        print("Predicted Waste Type:", prediction)
 
        if prediction.lower() == "unknown":
            return render_template('error_page.html')

        # --- Waste Information Database ---
        waste_info = {
            "E-waste": {
                "description": "Electronic waste like old phones, laptops, and circuit boards.",
                "disposal_method": "Send to certified e-waste recycling centers.",
                "recyclable": "Yes, about 90% components can be recovered.",
                "energy_used": "Consumes around 1.5 kWh per kg in recycling.",
                "water_usage": "Minimal water used in dismantling; chemical recycling uses ~10L/kg.",
                "hazards": "Contains lead, mercury, and cadmium which are toxic if untreated.",
                "recycling_benefit": "Recovers precious metals like gold, silver, and copper.",
                "co2_saving": "Recycling 1 ton saves ~1.5 tons CO₂ emissions.",
                "disposal_locations": [
                   "https://maps.google.com/?q=E-waste+Recycling+Center+Bangalore",
                    "https://maps.google.com/?q=E-waste+Disposal+Bangalore",
                    "https://maps.google.com/?q=E-waste+Drop+Point+Bangalore"
                    
                ]
            },
            "automobile wastes": {
                "description": "Scrap parts, oils, and batteries from vehicles.",
                "disposal_method": "Hand over to authorized automobile scrap dealers.",
                "recyclable": "Yes, ~75% of materials are recyclable.",
                "energy_used": "Around 2 kWh/kg for metal recovery and processing.",
                "water_usage": "~5L/kg during washing and material separation.",
                "hazards": "Toxic oil residues and lead acid from batteries.",
                "recycling_benefit": "Reuses metals, rubber, and plastics reducing landfill load.",
                "co2_saving": "Saves ~1.2 tons CO₂ per ton recycled.",
                "disposal_locations": [
                    "https://maps.google.com/?q=Automobile+Scrap+Yard+Bangalore",
                    "https://maps.google.com/?q=Auto+Recycle+Bangalore",
                    "https://maps.google.com/?q=Vehicle+Disposal+Bangalore"
                ]
            },
            "battery waste": {
                "description": "Used dry cells, lithium-ion, and lead-acid batteries.",
                "disposal_method": "Submit to battery recycling collection centers.",
                "recyclable": "Yes, up to 80% recoverable materials.",
                "energy_used": "1.2 kWh/kg due to chemical processing.",
                "water_usage": "~8L/kg for electrolyte neutralization.",
                "hazards": "Contains acid and heavy metals harmful to soil and water.",
                "recycling_benefit": "Recovers lithium, nickel, and zinc for reuse.",
                "co2_saving": "Recycling 1 ton saves 0.8 tons CO₂.",
                "disposal_locations": [
                     "https://maps.google.com/?q=Battery+Recycling+Bangalore",
                    "https://maps.google.com/?q=Battery+Collection+Center+Bangalore",
                    "https://maps.google.com/?q=Battery+Drop+Point+Bangalore"

                ]
            },
            "glass waste": {
                "description": "Bottles, windows, and other glass products.",
                "disposal_method": "Segregate by color and send to glass recycling units.",
                "recyclable": "100% recyclable with no loss in quality.",
                "energy_used": "0.7 kWh/kg to melt and reshape glass.",
                "water_usage": "~2L/kg for cleaning and cooling.",
                "hazards": "Non-toxic but can cause injury if mishandled.",
                "recycling_benefit": "Saves raw materials like sand and limestone.",
                "co2_saving": "Saves ~315 kg CO₂ per ton recycled.",
                "disposal_locations": [
                       
                       "https://maps.google.com/?q=+Recycling+Plant+Bangalore"
                    "Ewaste Hub  bengaluru karnataka","Saahas Waste Management Pvt Ltd bengaluru"
                ]
            },
            "light bulbs": {
                "description": "Fluorescent and LED bulbs.",
                "disposal_method": "Drop at lighting waste collection points.",
                "recyclable": "Yes, but requires careful handling for mercury lamps.",
                "energy_used": "0.5 kWh/unit for dismantling and separation.",
                "water_usage": "Negligible.",
                "hazards": "Mercury vapor in CFLs is toxic if broken.",
                "recycling_benefit": "Glass, metal, and plastic parts reused; mercury safely recovered.",
                "co2_saving": "Saves ~120 kg CO₂ per 1000 bulbs recycled.",
                "disposal_locations": [
                   "https://maps.google.com/?q=Light+Bulb+Recycling+Bangalore",
                    "https://maps.google.com/?q=Lighting+Disposal+Bangalore",
                    "https://maps.google.com/?q=CFL+Recycle+Bangalore"
                ]
            },
            "metal waste": {
                "description": "Iron, steel, aluminum scraps from industries or households.",
                "disposal_method": "Send to authorized metal scrap recyclers.",
                "recyclable": "100% recyclable.",
                "energy_used": "Recycling uses 75% less energy than producing new metal.",
                "water_usage": "~3L/kg in cooling and cleaning.",
                "hazards": "Rust and sharp edges pose safety risks.",
                "recycling_benefit": "Preserves natural ores and reduces mining.",
                "co2_saving": "Recycling 1 ton saves ~1.4 tons CO₂.",
                "disposal_locations": [
                     "https://maps.google.com/?q=Metal+Scrap+Yard+Bangalore",
                    "https://maps.google.com/?q=Metal+Recycling+Plant+Bangalore",
                    "https://maps.google.com/?q=Steel+Recycle+Center+Bangalore"
                ]

            },
            "organic waste": {
                "description": "Kitchen waste, food residues, and biodegradable matter.",
                "disposal_method": "Composting or biogas conversion.",
                "recyclable": "Fully recyclable through natural decomposition.",
                "energy_used": "Produces energy instead (biogas).",
                "water_usage": "~1L/kg during composting.",
                "hazards": "Can produce methane if landfilled.",
                "recycling_benefit": "Converts waste into compost and clean energy.",
                "co2_saving": "Reduces greenhouse gas by ~2 tons CO₂ per ton composted.",
                "disposal_locations": [
                     "https://maps.google.com/?q=Organic+Compost+Center+Bangalore",
                    "https://maps.google.com/?q=Food+Waste+Recycling+Bangalore",
                    "https://maps.google.com/?q=Biogas+Plant+Bangalore"

                ]
            },
            "paper waste": {
                "description": "Used papers, books, and cardboard.",
                "disposal_method": "Send to paper recycling mills or collection drives.",
                "recyclable": "Yes, up to 7 times before fiber degradation.",
                "energy_used": "Recycling uses 40% less energy than virgin paper production.",
                "water_usage": "Recycling uses 50% less water (~5L/kg).",
                "hazards": "Minimal environmental risk.",
                "recycling_benefit": "Saves trees, water, and landfill space.",
                "co2_saving": "Saves ~900 kg CO₂ per ton recycled.",
                "disposal_locations": [
                     "https://maps.google.com/?q=Paper+Recycling+Plant+Bangalore",
                    "https://maps.google.com/?q=Paper+Waste+Collection+Bangalore",
                    "https://maps.google.com/?q=Paper+Recycle+Bangalore"

                ]
            },
            "plastic waste": {
                "description": "PET bottles, wrappers, and containers.",
                "disposal_method": "Clean and segregate before sending to plastic recycling units.",
                "recyclable": "Partially recyclable depending on plastic type (1–7 codes).",
                "energy_used": "~2.5 kWh/kg for melting and reshaping.",
                "water_usage": "~6L/kg for cleaning and cooling.",
                "hazards": "Releases microplastics and toxins if burned or landfilled.",
                "recycling_benefit": "Reduces petroleum use and plastic pollution.",
                "co2_saving": "Saves ~1 ton CO₂ per ton recycled.",
                "disposal_locations": [
                     "https://maps.google.com/?q=Plastic+Recycling+Plant+Bangalore",
                
                    "https://maps.google.com/?q=Plastic+Waste+Collection+Bangalore"

                ]
            }
        }

        # --- Extract Details ---
        pred_type = prediction.lower().strip()
        details = waste_info.get(pred_type, {})

        description = details.get("description", "Information not available.")
        disposal_method = details.get("disposal_method", "Information not available.")
        recyclable = details.get("recyclable", "Information not available.")
        energy_used = details.get("energy_used", "N/A")
        water_usage = details.get("water_usage", "N/A")
        hazards = details.get("hazards", "N/A")
        recycling_benefit = details.get("recycling_benefit", "N/A")
        co2_saving = details.get("co2_saving", "N/A")
        disposal_locations = details.get("disposal_locations", [])
        from gtts import gTTS
        from pydub import AudioSegment
        import pygame
        import os

        text = str(details)
        language = 'en'


        # Create gTTS object
        tts = gTTS(text=text, lang=language, slow=False)

        # Save the converted audio in a file
        tts.save("output.mp3")
        print("Audio file saved successfully.")
    
        pygame.mixer.init()

        # Load the audio file
        pygame.mixer.music.load("output.mp3")

        # Play the audio file
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Adjust the tick value as needed

        # Close the mixer
        pygame.mixer.quit()
        # --- Save to CSV (Database) ---
        csv_file = 'waste_data.csv'
        columns = [
            'user_id', 'waste_type', 'date', 'description', 'disposal_method',
            'recyclable', 'energy_used', 'water_usage', 'hazards',
            'recycling_benefit', 'co2_saving', 'disposal_locations'
        ]

        if not os.path.exists(csv_file):
            df = pd.DataFrame(columns=columns)
        else:
            df = pd.read_csv(csv_file)

        current_date = datetime.now().strftime("%Y-%m-%d")

        new_data = {
            'user_id': user_id,
            'waste_type': pred_type,
            'date': current_date,
            'description': description,
            'disposal_method': disposal_method,
            'recyclable': recyclable,
            'energy_used': energy_used,
            'water_usage': water_usage,
            'hazards': hazards,
            'recycling_benefit': recycling_benefit,
            'co2_saving': co2_saving,
            'disposal_locations': "; ".join(disposal_locations)
        }

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(csv_file, index=False)

        # --- Render Result Page ---
        return render_template(
            'rust-result.html',
            prediction=prediction.capitalize(),
            description=description,
            disposal_method=disposal_method,
            recyclable=recyclable,
            energy_used=energy_used,
            water_usage=water_usage,
            hazards=hazards,
            recycling_benefit=recycling_benefit,
            co2_saving=co2_saving,
            disposal_locations=disposal_locations,
            title="Waste Identification Result"
        )

    return render_template('rust2.html', title=title)




# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=True)
