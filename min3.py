# -*- coding: utf-8 -*-
import streamlit as st
#
from datetime import date
import requests
from bs4 import BeautifulSoup

def main():
    mode = st.sidebar.radio('Choose mode',
        ['Mode a', 'Mode b'])

    if mode == 'Mode a':
        mode_a()
    elif mode == 'Mode b':
        mode_b()

def mode_a():
    st.title('Mode A')

    st.header(f'自由時報熱門新聞 {date.today()}')

    res = requests.get('https://www.ltn.com.tw/')
    soup = BeautifulSoup(res.text, 'html.parser')

    hot_list = soup.select('.week_hot li')
    img_list = [s.find('img')['src'] for s in hot_list]
    cap_list = [s.find('a', class_='title').text for s in hot_list]

    st.image(img_list, caption=cap_list, width=300)

def mode_b():
    st.title('Mode B')

    raw_text = st.text_input('Text', 'D3lab')
    times = st.number_input('Multiple times', min_value=0, value=0)

    styles = st.multiselect('Choose Style', ['header', 'bold', 'color'])

    text = raw_text * times
    if 'bold' in styles:
        text = f'**{text}**'
    if 'color' in styles:
        color = st.beta_color_picker('Pick A Color', '#00f900')
        text = f'<span style="color: {color}">{text}</span>'
    if 'header' in styles:
        text = f'## {text}'

    st.markdown(text, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
