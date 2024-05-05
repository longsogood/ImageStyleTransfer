from torch_snippets import *
from PIL import Image

device = 'cuda' if torch.cuda.is_available() else 'cpu'
IMAGE_SIZE = 256
transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])

class Pix2PixDataset(Dataset):
    def __init__(self, root):
        self.files = Glob(root, silent=True)
        # print(self.files)
        logger.info(f'Loaded {len(self)} files')
    def __getitem__(self, idx):
        img = cv2.imread(str(self.files[randint(len(self))]))[...,::-1]
        h, w, _ = img.shape
        img_src = Image.fromarray(img[:,:w//2])
        img_trg = Image.fromarray(img[:,w//2:])
        return img_src, img_trg

    # let's restrict to the first few files only
    def __len__(self): return min(10000, len(self.files))
    def choose(self): return self[randint(len(self))]

    
    def collate_fn(self, batch):
        srcs, trgs = list(zip(*batch))

        srcs = torch.cat([transform(img)[None] for img in srcs], 0).to(device).float()
        trgs = torch.cat([transform(img)[None] for img in trgs], 0).to(device).float()
        return srcs.to(device), trgs.to(device)