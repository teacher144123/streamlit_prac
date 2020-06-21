import streamlit as st

import pandas as pd
import numpy as np
import altair as alt

st.write('# Some Example')
st.write('**Let\'s Makrdown!**')


df = pd.DataFrame(
    np.random.randn(200, 3),
    columns=['a', 'b', 'c'])
df
#
st.write(sorted)
st.write({'a': 'apple', 'b': 'banana', 'c': ['cat', 'cave', 'category']})

c = alt.Chart(df).mark_circle().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

st.write(c)
