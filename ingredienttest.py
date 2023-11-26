import streamlit as st

ingredients  = "ranking | [['Rice Flour',1], ['Sugar',2], ['Baking Soda',3], ['Sodiumaluminum Phosphate',3], ['Monocalciumphosphate',3], ['Modified Potato Starch',4], ['Salt',5], ['Xanthan Gum',7]] | 5"
split_ingredients = ingredients.split("|")[1]
in1 = eval(split_ingredients)
st.dataframe(data = in1, hide_index = True, column_config = {"0":"ingredient", 
                                                             "1": st.column_config.ProgressColumn("score", min_value = 0, max_value = 10, format= "%d") })