import streamlit as st
from data_loader import load_data
from engine import get_recommendations

st.set_page_config(page_title="REC-Cart", layout="wide", initial_sidebar_state="collapsed")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    .stTextInput > div > div > input { background-color: #111 !important; color: white !important; border-radius: 30px !important; }
    .product-card {
        border: 1px solid #222; padding: 20px; border-radius: 20px;
        background: rgba(255, 255, 255, 0.03); text-align: center; margin-bottom: 25px;
    }
    .header-box {
        text-align: center; padding: 40px; border-radius: 0 0 40px 40px; margin-bottom: 40px;
        background: linear-gradient(180deg, rgba(0,209,255,0.1) 0%, transparent 100%);
    }
    div.stButton > button { background: transparent; color: #00D1FF; border: 1px solid #00D1FF; border-radius: 12px; width: 100%; }
    div.stButton > button:hover { background: #00D1FF; color: black; }
    </style>
""", unsafe_allow_html=True)

df = load_data()

# --- INITIALIZE SESSION STATE ---
if "current_item" not in st.session_state:
    st.session_state.current_item = None
if "show_dialog" not in st.session_state:
    st.session_state.show_dialog = False

# --- DIALOG DEFINITION ---
@st.dialog("PRODUCT DETAILS", width="large")
def show_details_dialog():
    item = st.session_state.current_item
    
    col_img, col_info = st.columns([1, 1])
    with col_img:
        st.image(item['image_url'], use_container_width=True)
    with col_info:
        st.write(f"## {item['name']}")
        st.write(f":gray[Brand:] **{item['brand']}**")
        st.markdown(f"<h2 style='color:#00D1FF'>₹{int(item['price']) * 83}</h2>", unsafe_allow_html=True)
        st.write("---")
        st.write(item['description'])
        if st.button("🚀 ADD TO CART"):
            st.success("Added to Cart!")
    
    st.write("---")
    st.subheader("Similar Products")
    
    recs = get_recommendations(item['name'], df)
    if not recs.empty:
        r_cols = st.columns(4)
        for i, (_, r_row) in enumerate(recs.iterrows()):
            with r_cols[i]:
                st.image(r_row['image_url'], use_container_width=True)
                st.caption(r_row['name'])
                # Click logic: Update state and rerun
                if st.button("EXPLORE", key=f"rec_{r_row['id']}"):
                    st.session_state.current_item = r_row
                    st.rerun() # This triggers the script to re-check 'st.session_state.show_dialog'

# --- HEADER ---
st.markdown("""
    <div class="header-box">
        <img src="https://cdn-icons-png.flaticon.com/512/3144/3144456.png" width="60">
        <h1 style="margin: 10px 0 0 0; letter-spacing: 5px; font-weight: 900;">REC-<span style="color:#00D1FF">CART</span></h1>
        <p style="color: #666; letter-spacing: 2px;">PRODUCT RECOMMENDATION SYSTEM</p>
    </div>
""", unsafe_allow_html=True)

# --- SEARCH ---
_, c2, _ = st.columns([1, 2, 1])
with c2:
    query = st.text_input("", placeholder="Search Gear, Apparel, or Electronics...")

# --- GRID DISPLAY ---
display_df = df[df['name'].str.contains(query, case=False) | df['tags'].str.contains(query, case=False)] if query else df

idx = 0
for _ in range(len(display_df) // 4 + 1):
    cols = st.columns(4)
    for c in range(4):
        if idx < len(display_df):
            row = display_df.iloc[idx]
            with cols[c]:
                st.markdown(f"""
                    <div class="product-card">
                        <img src="{row['image_url']}" style="width:100%; height:200px; object-fit:cover; border-radius:10px; margin-bottom:15px;">
                        <div style="height: 50px; overflow: hidden;"><b>{row['name']}</b></div>
                        <p style="color:#00D1FF; font-size:18px;">₹{int(row['price']) * 83}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("VIEW DETAILS", key=f"main_{row['id']}"):
                    st.session_state.current_item = row
                    st.session_state.show_dialog = True
                    st.rerun()
            idx += 1

# --- PERSISTENT DIALOG TRIGGER ---
# This is the "Magic" part. It checks every rerun if it SHOULD be showing a dialog.
if st.session_state.show_dialog:
    show_details_dialog()
    # If the user closes the dialog by clicking outside, we need to reset the state
    # But usually, it stays True until we manually set it False.