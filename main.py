import re
import sys
import csv

from PIL import Image
import streamlit as st
import pytesseract

matcher = re.compile(r'(\d+)% ([a-zA-Z]+)')

def calculate_sustainability_score(image):
  txt = pytesseract.image_to_string(Image.open(image))
  groups = matcher.findall(txt)
  for group in groups:
    print(group)
  return 8

def main():
  st.title("Sustainable Shopping Suggester")

  # Show upload image option
  uploaded_files = st.file_uploader("Please upload a fabric content tag: ", accept_multiple_files=True)
  
  # Store scores
  idx, max_score = -1, sys.float_info.min

  cols = st.columns(len(uploaded_files)) if uploaded_files else list()

  # Calculate score for each file
  for id, uploaded_file in enumerate(uploaded_files):
      # To read file as bytes:
      bytes_data = uploaded_file.read()
      
      # Display uploaded image
      with cols[id]:
        st.write(f"{id + 1}")
        st.image(bytes_data, use_column_width=True)

      # Function to parse and get fabric contents
      sustainability_score = calculate_sustainability_score(uploaded_file)

      if max_score < sustainability_score:
        idx, max_score = id, sustainability_score

      st.write(f"#### The sustainability score of cloth {id + 1} is :: {sustainability_score}")

  if idx != -1:
    st.write(f"### {idx + 1} is the best according to our sustainibility rating of {max_score}.")


if __name__ == "__main__":
  main()