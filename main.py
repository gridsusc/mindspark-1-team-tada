import re
import csv
import sys
from PIL import Image
import streamlit as st
import pytesseract


def calculate_sustainability_score(percentages_materials, material_scoring_dict):
  # Calculate score for the whole item
  sustainability_score = 0.0

  for percentage_material in percentages_materials:
    percentage, material = float(percentage_material[0]) / 100, percentage_material[1].lower()
    if material in material_scoring_dict:
      sustainability_score += (percentage * material_scoring_dict[material])
  
  return sustainability_score

def main(material_scoring_dict):
  matcher = re.compile(r'(\d+)% ([a-zA-Z]+)')

  st.title("Sustainable Shopping Suggester")

  # Show upload image option
  uploaded_files = st.file_uploader("Please upload a fabric content tag: ", accept_multiple_files=True)
  
  # Store scores
  idx, max_score = -1, -sys.float_info.max

  items = list()

  sustainability_scores = list()

  # Calculate score for each file
  for id, uploaded_file in enumerate(uploaded_files):
    items.append(uploaded_file.read())
    
    txt = pytesseract.image_to_string(Image.open(uploaded_file))

    groups = matcher.findall(txt)

    # Function to parse and get fabric contents
    sustainability_score = calculate_sustainability_score(groups, material_scoring_dict)

    sustainability_scores.append(sustainability_score)

    if max_score < sustainability_score:
      idx, max_score = id, sustainability_score

  if idx != -1:
    st.write(f"### Best Item {idx + 1:02d} with sustainability score {max_score:.02f}.")

  if uploaded_files:
    with st.container():

      cols = st.columns(len(uploaded_files)) if uploaded_files else list()
      
      for idx in range(len(sustainability_scores)):
        col, item, sustainability_score = cols[idx], items[idx], sustainability_scores[idx]
        
        # Display uploaded image
        with col:
          st.write(f"Item {idx + 1:02d} Score {sustainability_score:.02f}")
          st.image(item, caption=f"Item {id + 1:02d}", width=250)


if __name__ == "__main__":

  material_scoring_dict = dict()
  with open('./material_scoring.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=",")
    for row in csv_reader:
      material_scoring_dict[row[0].lower()] = float(row[1])

  main(material_scoring_dict)