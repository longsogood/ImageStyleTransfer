import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import streamlit as st
# --- USER AUTHENTICATION ---
# names = ["Du Hoang Huy"]
# usernames = ['huydu88']

# load hashed passwords
# file_path = Path(__file__).parent / "hashed_pw.pkl"
# # with file_path.open("rb") as file:
    # hashed_passwords = pickle.load(file)
login_dict = { 'Form name': 'Đăng nhập','Username': 'Username','Password': 'Password','Login': 'Đăng nhập' }
with open('login_info.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
st.image('images\large_phenikaa_logo.jpg')

name, authentication_status, username = authenticator.login(fields = login_dict)

if st.session_state['authentication_status'] == False:
    # st.session_state.authentication_status=False
    st.error("Username/password is incorrect")

if st.session_state['authentication_status'] == None:
    # st.session_state.authentication_status=False
    st.warning("Vui lòng nhập username và password")

if st.session_state['authentication_status']:
    # st.session_state.authentication_status=True
    st.info(f'Welcome,{name}!')
    authenticator.logout('logout','sidebar')