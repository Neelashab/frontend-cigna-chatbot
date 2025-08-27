import streamlit as st

main_menu = st.Page("./app-pages/main_menu.py", title="Home", default=True)
individual_chat = st.Page("./app-pages/individual_chat.py", title="Individual Chat")
business_chat = st.Page("./app-pages/business_chat.py", title="Business Chat")
about_page = st.Page("./app-pages/about_page.py", title="About")

# Set up navigation
pg = st.navigation([main_menu, individual_chat, business_chat, about_page])

# Run the selected page
pg.run()

