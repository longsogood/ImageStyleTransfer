from utils import sample_prediction
from model import GeneratorUNet
from dataset import Pix2PixDataset
from torchvision import transforms
from torch_snippets import *

device = 'cuda' if torch.cuda.is_available() else 'cpu'
INIT_WEIGHT = False
IMAGE_SIZE = 256
transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])

val_ds = Pix2PixDataset('data\edges2shoes\\val')
val_dl = DataLoader(dataset=val_ds, batch_size=1, shuffle=True, collate_fn=val_ds.collate_fn)

generator = GeneratorUNet().to(device)
generator.load_state_dict(torch.load('models\generator.pth'))

sample_prediction(generator, val_dl)