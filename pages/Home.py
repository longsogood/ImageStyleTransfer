import streamlit as st
import pandas as pd
import pickle
from pathlib import Path

if st.session_state['authentication_status'] == False or st.session_state['authentication_status'] == None:
    st.warning('Vui lòng đăng nhập để truy cập')
else:
    # st.sidebar.image("images\logo.png", use_column_width=True)
    st.title("Ứng dụng chuyển đổi từ ảnh vẽ sang ảnh thật")
    st.write("Chào mừng bạn đến với ứng dụng chuyển đổi độc đáo của chúng tôi - một công cụ mạnh mẽ \
            để biến những bức tranh vẽ tay của bạn thành hình ảnh thực tế sống động. Với sự tiến bộ \
            trong công nghệ trí tuệ nhân tạo và học sâu, ứng dụng của chúng tôi đã được phát triển \
            để đưa ra trải nghiệm độc đáo và tuyệt vời cho các nghệ sĩ và người dùng.")
    st.image("images\example_image_home.jpg", caption="Ví dụ cho ứng dụng của chúng tôi", )

    st.header("Author")
    df = pd.DataFrame([['Hoàng Huy Du','88888888']],columns=['Sinh viên','MSSV'])
    st.table(df)
