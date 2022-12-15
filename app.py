import streamlit as st
import os
import time
import main

st.sidebar.markdown("### App Info")
st.sidebar.markdown(
    "This web app is build using Python's opencv module. Upload the image of a sudoku puzzle to solve it")

st.title("Real Time Sudoku Solver")

image_file = st.file_uploader(label="Add image here",type=['png'])

if image_file is not None:
    with open(os.path.join("utils",image_file.name),"wb") as f: 
      f.write(image_file.getbuffer())      
    os.rename(os.path.join("utils",image_file.name), os.path.join("utils", "suduko.png"))   
    st.success("Saved File")

    with st.spinner('Processing...'):
        main.main()
        st.write(main.return_sudoku())
        st.image("solved.png")

    st.success('Done!')

    os.remove(os.path.join("utils", "suduko.png"))

