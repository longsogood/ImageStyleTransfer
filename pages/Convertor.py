import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from torch_snippets import *
from torchvision import transforms
from model import GeneratorUNet
from torchvision.utils import save_image
import streamlit_authenticator as stauth    
# set parameters
device = 'cuda' if torch.cuda.is_available() else 'cpu'
INIT_WEIGHT = False
IMAGE_SIZE = 256
transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])
detransform = transforms.Compose([
                transforms.Normalize((-1, -1, -1), (2, 2, 2)),
                transforms.ToPILImage()
            ])

denorm = transforms.Normalize((-1, -1, -1), (2, 2, 2))
# Load model
model = GeneratorUNet().to(device)
model.load_state_dict(torch.load('models\generator.pth'))
model.to(device)

if st.session_state['authentication_status'] == False or st.session_state['authentication_status'] == None:
    st.warning('Vui lòng đăng nhập để truy cập')
else:

    col1_width = 0.4
    col2_width = 0.2
    col3_width = 0.4

    # Canvas parameters
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", ("point", "freedraw", "line", "rect", "circle", "transform")
    )
    
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == 'point':
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
    realtime_update = st.sidebar.checkbox("Update in realtime", True)

    # Logo
    st.image('images\large_phenikaa_logo.jpg')

    # Title
    st.markdown("<h1 style='text-align: center; color: black;'>Image2Image Style Transfer Application</h1>", unsafe_allow_html=True)


    st.write('#')

    # Select box
    select_box = st.selectbox("Lựa chọn:", options=['Upload file','Draw'])

    # Create columns
    col1, col2, col3 = st.columns([col1_width, col2_width, col3_width])



    if select_box == "Draw":
        with col1:
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=stroke_width,
                stroke_color=stroke_color,
                background_color=bg_color,
                background_image=Image.open(bg_image) if bg_image else None,
                update_streamlit=realtime_update,
                height=256,
                width=256,
                drawing_mode=drawing_mode,
                point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
                key="canvas",
            )
        
    else:
        with col1:
            uploaded_file = st.file_uploader("Nhấn để chọn ảnh hoặc kéo thả ảnh vào đây", type=['png','jpg'], label_visibility="collapsed")
            if uploaded_file is not None:
                # bytes_data = uploaded_file.getvalue()
                bytes_data = Image.open(uploaded_file)
                st.image(bytes_data)

    with col2:
        # row1, row2, row3 = st.rows
        change_button = st.button('Change')

    with col3:
        if change_button:
            if select_box == "Draw" and canvas_result.image_data is not None:
                # st.text(canvas_result.background_image)
                input = Image.fromarray(canvas_result.image_data).convert("RGB")
                input = transform(input)
                input = input.unsqueeze(0)
                input = input.cuda()
                save_image(input,'pic.png')
                
                # st.write("#")
                # st.image(pic)
                with torch.no_grad():
                    # st.text(input.shape)
                    output = model(input)
                    # st.text(output.shape)
                    save_image(output.squeeze(0),'output.png')
                    output = detransform(output.squeeze(0)).convert("RGBA")
                    st.write("#")
                    st.image(output)

            if select_box == "Upload file" and uploaded_file is not None:
                input = transform(bytes_data)
                input = input.unsqueeze(0)
                input = input.cuda()
                save_image(input,'upload_file_pic.png')

                with torch.no_grad():
                    output = model(input)
                    save_image(output.squeeze(0),'upload_file_output.png')
                    output = detransform(output.squeeze(0)).convert("RGBA")
                    st.image(output)
    # Chuyển ảnh vẽ qua model xử lý và đưa ra output
              