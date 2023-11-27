import streamlit as st

ingredients  = " Ranking | [['Romaine Lettuce',5], ['Cucumber',4], ['Grape Tomatoes',4], ['Hard-cooked Eggs',6], ['Red Bell Pepper',5], ['Carrot',3], ['Cheddar Cheese',6], [Pasteurized Milk Cultures,1], [Salt,1], [Enzymes,1], [Annatto,1], [Potato,2], [Pepper,1], [Powered Cellulose,1], [Starch,1], [Natamycin,1]] | 8 "
split_ingredients = ingredients.split("|")[1]
in1 = eval(split_ingredients)
st.dataframe(data = in1, hide_index = True, column_config = {"0":"ingredient", 
                                                             "1": st.column_config.ProgressColumn("score", min_value = 0, max_value = 10, format= "%d") })