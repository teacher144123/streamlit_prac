import streamlit as st
#
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import transforms
import numpy as np
import os, math
from PIL import Image

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.mp = nn.MaxPool2d(2)
        self.fc = nn.Linear(320, 10)

    def forward(self, x):
        in_size = x.size(0)

        x = self.mp(self.conv1(x))
        x = F.relu(x)
        x = self.mp(self.conv2(x))
        x = F.relu(x)
        x = x.view(in_size, -1)
        x = self.fc(x)

        return x

@st.cache
def predict(p):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    device = torch.device(device)

    @st.cache
    def load_model():
        model = SimpleCNN()
        model = model.to(device)
        model.load_state_dict(torch.load('./MNIST_CNN_model.pt',
                                map_location=device))
        return model

    @st.cache
    def load_img(p):
        trans = transforms.Compose([
            transforms.RandomCrop(28),
            transforms.ToTensor(),
        ])
        data = Image.open(p).convert('L')
        data = trans(data).unsqueeze(0)
        data = 1 - data

        return data

    model = load_model()
    data = load_img(p).to(device)

    out = model(data).cpu()
    return out.max(1)[1].item(), out.detach()

def main():
    global show_emb

    st.sidebar.title('App mode')
    app_mode = st.sidebar.radio('App mode', ('Exist IMG', 'Upload IMG'))
    show_emb = st.sidebar.checkbox('Show predictd probability')

    if app_mode == 'Exist IMG':
        exist_img()
    elif app_mode == 'Upload IMG':
        upload_img()


def exist_img():
    st.title('Exist IMG')

    files = ['./datas/' + f for f in os.listdir('./datas')]
    st.write('All imgs')
    st.image(files, width=50)

    p_choose = st.slider('Choose Index', 0, len(files) - 1)

    st.write(f'Choose index {p_choose}')
    st.image(files[p_choose], width=100)

    pred, emb = predict(files[p_choose])
    if show_emb:
        emb = torch.softmax(emb, 1)
        emb = emb.numpy().reshape(-1, 1)
        st.write(emb)
    st.write(f'Predicted {pred}')

def upload_img():
    st.title('Upload IMG')

    img_f = st.file_uploader('Choose IMG')

    if img_f:
        st.image(img_f, width=100)

        pred, emb = predict(img_f)
        if show_emb:
            emb = torch.softmax(emb, 1)
            emb = emb.numpy().reshape(-1, 1)
            emb = np.floor(emb * 100) / 100
            st.write(emb)
        st.write(f'Predicted {pred}')

if __name__ == '__main__':
    main()
