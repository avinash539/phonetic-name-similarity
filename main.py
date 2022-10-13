import streamlit as st
import pandas as pd
import random
import operator
from phonetic_ipa import compare_similarity

st.markdown("""
<style>
.css-14xtw13.e8zbici0{
    visibility: hidden;
}
.css-1lsmgbg.egzxvld0{
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

st.title("Phonetically name correction")

data = pd.DataFrame()
score_list = []
# pincode = st.empty()
area_name = st.empty()

if 'pincode' not in st.session_state:
    st.session_state.pincode = ''


@st.cache
def load_data():
    if 'pincode' in st.session_state and st.session_state.pincode:
        df = pd.read_csv('Locality_village_pincode_final_mar-2017.csv', encoding="ISO-8859-1")
        return df[df.Pincode == int(st.session_state.pincode)].drop_duplicates().reset_index(drop=True)


def get_random_pincode():
    df = pd.read_csv("Locality_village_pincode_final_mar-2017.csv", encoding="ISO-8859-1")
    st.session_state.pincode = random.choice(df.Pincode.tolist())


pincode_col, area_col = st.columns(2)
with pincode_col:
    st.session_state.pincode = pincode_col.text_input("Pincode", value=st.session_state.pincode, max_chars=6,
                                                      type="default",
                                                      placeholder="Enter Pincode", key="numeric",
                                                      label_visibility="visible")

pincode_name_col, random_btn_col = st.columns([1, 2.5])
pincode_name_col.write(f'Entered Pincode: {st.session_state.pincode}')
random_button = random_btn_col.button("Random Pincode", on_click=get_random_pincode)

if 'pincode' in st.session_state and st.session_state.pincode:
    data = load_data()
    st.write(f"Total records found: {data.shape[0]}")
    st.dataframe(data, height=200)

with area_col:
    if area_name := area_col.text_input("Area", type="default", placeholder="Enter Incorrect Area Name",
                                        label_visibility="visible"):
        if data.shape[0]:
            if score_list := compare_similarity(area_name, data["Village/Locality name"].tolist()):
                st.sidebar.title('Scores of the phonetic similarity')
                score_dict = {row["Village/Locality name"]: round(score_list[i], 3) for i, row in data.iterrows()}
                score_dict = dict(sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True))
                st.sidebar.write(score_dict)

if score_list:
    st.write(f'##### Most phonetically similar records for "{area_name}" are:')
    index = score_list.index(max(score_list))
    match_area_name = data[data.index == index]["Village/Locality name"].reset_index(drop=True).loc[0]
    match = data[data["Village/Locality name"] == match_area_name]
    st.write(match)
