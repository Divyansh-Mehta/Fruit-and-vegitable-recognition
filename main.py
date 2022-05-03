import streamlit as st
from PIL import Image
from keras.preprocessing.image import load_img,img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup

model = load_model('FV.h5')
labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot', 7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger', 14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple', 26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn', 32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

fruits = ['Apple','Banana','Bello Pepper','Chilli Pepper','Grapes','Jalepeno','Kiwi','Lemon','Mango','Orange','Paprika','Pear','Pineapple','Pomegranate','Watermelon']
vegetables = ['Beetroot','Cabbage','Capsicum','Carrot','Cauliflower','Corn','Cucumber','Eggplant','Ginger','Lettuce','Onion','Peas','Potato','Raddish','Soy Beans','Spinach','Sweetcorn','Sweetpotato','Tomato','Turnip']

def fetch_calories(prediction):
    try:
        url = 'https://www.google.com/search?&q=calories in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return calories
    except Exception as e:
        st.error("Can't able to fetch the Calories")
        print(e)

def processed_img(img):
    img=img_to_array(img)
    img=img/255
    img=np.expand_dims(img,0)
    answer=model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()

def run():
    st.title("CaLoRie EstiMatOr")
    img_file = st.file_uploader("Upload Image", type=["jpg", "png"])
    predict = None
    if img_file is not None:
        img = Image.open(img_file).resize((224,224))
        st.image(img,use_column_width=False)
        result= processed_img(img)
        print(result)
        ctg = None
        if result in vegetables:
            ctg = "vegetable"
            st.info('**Category : Vegetables**')
        else:
            ctg = "Fruit"
            st.info('**Category : Fruit**')
        st.success('**' + ctg +' : ' + result+ '**')
        margin1, pre, margin2 = st.columns([2,1,2])
        predict = pre.button("Find Calories")
        if predict:
            cal = fetch_calories(result)
            if cal:
                st.warning('**' + cal + '(100 grams)**')

rad = st.sidebar.radio("Navigation", ["Home", "About", "Calorie Estimator"])
if rad == "Home":
    st.text("Hi")
if rad == "About":
    st.text("hi again")
if rad == "Calorie Estimator":
    run()
