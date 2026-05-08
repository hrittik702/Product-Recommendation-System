import streamlit as st
from data_loader import load_data
from engine import get_recommendations

st.set_page_config(page_title="REC-Cart | Omnitrix AI", layout="wide", initial_sidebar_state="collapsed")


st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Neon Green Header */
    .header-box {
        text-align: center;
        padding: 30px;
        background: linear-gradient(180deg, rgba(22, 174, 88, 0.2) 0%, transparent 100%);
        border-bottom: 3px solid #16AE58;
        border-radius: 0 0 40px 40px;
        margin-bottom: 40px;
    }

    /* Search Bar Styling */
    .stTextInput > div > div > input {
        background-color: #111 !important;
        color: #C6E115 !important;
        border: 1px solid #16AE58 !important;
        border-radius: 30px !important;
    }

    /* Product Cards */
    .product-card {
        border: 1px solid #16AE58;
        padding: 15px;
        border-radius: 20px;
        background: rgba(22, 174, 88, 0.05);
        text-align: center;
        transition: 0.3s ease;
        margin-bottom: 20px;
    }
    .product-card:hover {
        box-shadow: 0px 0px 20px #16AE58;
        transform: scale(1.02);
    }
    
    /* Price and Text */
    .price-tag { color: #C6E115; font-size: 20px; font-weight: bold; }
    
    /* Global Button Styling */
    div.stButton > button {
        border-radius: 10px;
        transition: 0.3s;
        font-weight: bold;
    }
    
    /* Primary View Button */
    .main-btn > div > button {
        background-color: transparent;
        color: #16AE58;
        border: 1px solid #16AE58;
    }
    
    /* Like Button Styling */
    .like-btn > div > button {
        color: #FF4B4B !important;
        border: 1px solid #FF4B4B !important;
    }
    </style>
""", unsafe_allow_html=True)

df = load_data()

if "current_item" not in st.session_state:
    st.session_state.current_item = None
if "show_dialog" not in st.session_state:
    st.session_state.show_dialog = False
if "liked_items" not in st.session_state:
    st.session_state.liked_items = []


@st.dialog("PRODUCT DETAILS", width="large")
def product_popup():
    item = st.session_state.current_item
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.image(item['image_url'], use_container_width=True)
        
    with col_b:
        st.write(f"## {item['name']}")
        st.write(f":gray[Brand:] **{item['brand']}**")
        st.markdown(f"<div class='price-tag'>₹{int(item['price']) * 83}</div>", unsafe_allow_html=True)
        st.write("---")
        st.write(item['description'])
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🛒 ADD TO CART", key=f"cart_{item['id']}"):
                st.toast(f"{item['name']} added to cart!")
        with btn_col2:
            is_liked = item['name'] in st.session_state.liked_items
            label = "❤️ LIKED" if is_liked else "🤍 LIKE"
            if st.button(label, key=f"popup_like_{item['id']}"):
                if not is_liked:
                    st.session_state.liked_items.append(item['name'])
                    st.toast("Saved to your interests!")
                    st.rerun()

    st.write("---")
    st.subheader("🧬 Related DNA (Recommendations)")
    
    recs = get_recommendations(item['name'], df)
    if not recs.empty:
        r_cols = st.columns(4)
        for i, (_, r_row) in enumerate(recs.iterrows()):
            with r_cols[i]:
                st.image(r_row['image_url'], use_container_width=True)
                st.caption(f"**{r_row['name']}**")
                if st.button("EXPLORE", key=f"rec_{r_row['id']}"):
                    st.session_state.current_item = r_row

st.markdown("""
    <div class="header-box">
        <h1 style="margin: 0; letter-spacing: 7px; font-weight: 900; color: #16AE58;">
            REC-<span style="color:#C6E115">CART</span>
        </h1>
        <p style="color: #666; letter-spacing: 3px; font-size: 14px;">PRODUCT RECOMMENDATION SYSTEM</p>
    </div>
""", unsafe_allow_html=True)


_, mid, _ = st.columns([1, 2, 1])
with mid:
    query = st.text_input("", placeholder="Search for products across the gallery...")


if st.session_state.liked_items:
    st.write("### ✨ Inspired by Your Likes")
    last_liked = st.session_state.liked_items[-1]
    p_recs = get_recommendations(last_liked, df)
    p_cols = st.columns(5)
    for i, (_, p_row) in enumerate(p_recs.head(5).iterrows()):
        with p_cols[i]:
            st.image(p_row['image_url'], use_container_width=True)
            if st.button("VIEW", key=f"pers_{p_row['id']}"):
                st.session_state.current_item = p_row
                st.session_state.show_dialog = True
                st.rerun()
    st.divider()


display_df = df[df['name'].str.contains(query, case=False) | df['tags'].str.contains(query, case=False)] if query else df

idx = 0
rows = (len(display_df) // 4) + 1
for _ in range(rows):
    cols = st.columns(4)
    for c in range(4):
        if idx < len(display_df):
            row = display_df.iloc[idx]
            with cols[c]:
                st.markdown(f"""
                    <div class="product-card">
                        <img src="{row['image_url']}" style="width:100%; height:180px; object-fit:cover; border-radius:12px; margin-bottom:10px;">
                        <div style="height: 45px; overflow: hidden; font-size:14px; margin-bottom:5px;"><b>{row['name']}</b></div>
                        <p class="price-tag">₹{int(row['price']) * 83}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("VIEW DETAILS", key=f"main_{row['id']}"):
                    st.session_state.current_item = row
                    st.session_state.show_dialog = True
                    st.rerun()
            idx += 1


if st.session_state.show_dialog:
    product_popup()