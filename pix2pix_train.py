import os
from torch_snippets import *
from pytorch_model_summary import summary
from torchvision import transforms
from PIL import Image
from dataset import Pix2PixDataset
from utils import prediction_plot, weights_init
from model import GeneratorUNet, Discriminator
import time
TRAIN_FROM_SRATCH = False
device = 'cuda' if torch.cuda.is_available() else 'cpu'

IMAGE_SIZE = 256
transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])

trn_ds = Pix2PixDataset('data\edges2shoes\\train')
val_ds = Pix2PixDataset('data\edges2shoes\\val')

trn_dl = DataLoader(trn_ds, batch_size=32, shuffle=True, collate_fn=trn_ds.collate_fn)


generator = GeneratorUNet().to(device)
discriminator = Discriminator().to(device)

print(summary(generator, torch.zeros(3, 3, IMAGE_SIZE, IMAGE_SIZE).to(device)))
print(summary(discriminator, torch.zeros(3, 3, IMAGE_SIZE, IMAGE_SIZE).to(device), torch.zeros(3, 3, IMAGE_SIZE, IMAGE_SIZE).to(device)))

def discriminator_train_step(real_src, real_trg, fake_trg):
    discriminator.train()
    d_optimizer.zero_grad()

    prediction_real = discriminator(real_trg, real_src)
    error_real = criterion_GAN(prediction_real, torch.ones(len(real_src), 1, 16, 16).cuda())
    error_real.backward()

    prediction_fake = discriminator(fake_trg.detach(), real_src)
    error_fake = criterion_GAN(prediction_fake, torch.zeros(len(real_src), 1, 16, 16).cuda())
    error_fake.backward()

    d_optimizer.step()

    return error_real + error_fake, prediction_real, prediction_fake

def generator_train_step(real_src, fake_trg):
    discriminator.train()
    g_optimizer.zero_grad()
    prediction = discriminator(fake_trg, real_src)

    loss_GAN = criterion_GAN(prediction, torch.ones(len(real_src), 1, 16, 16).cuda())
    loss_pixel = criterion_pixelwise(fake_trg, real_trg)
    loss_G = loss_GAN + lambda_pixel * loss_pixel

    loss_G.backward()
    g_optimizer.step()
    return loss_G

# generator = GeneratorUNet().to(device)
# discriminator = Discriminator().to(device)
if TRAIN_FROM_SRATCH:
    print("Train from scratch!")
    generator.apply(weights_init)
    discriminator.apply(weights_init)
else:
    print("Load trained weights!")
    generator.load_state_dict(torch.load('models\generator.pth'))
    discriminator.load_state_dict(torch.load('models\discriminator.pth'))
    
criterion_GAN = torch.nn.MSELoss()
criterion_pixelwise = torch.nn.L1Loss()

lambda_pixel = 100
g_optimizer = torch.optim.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
d_optimizer = torch.optim.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))

val_dl = DataLoader(val_ds, batch_size=1, shuffle=True, collate_fn=val_ds.collate_fn)

epochs = 3
for epoch in range(epochs):
    N = len(trn_dl)
    for bx, batch in enumerate(trn_dl):
        
        start = time.time()
        real_src, real_trg = batch
        fake_trg = generator(real_src)
        
        errD, d_loss_real, d_loss_fake = discriminator_train_step(real_src, real_trg, fake_trg)
        errG = generator_train_step(real_src, fake_trg)
        print("Epoch:",epoch+1," errD:", errD.item(), " errG:", errG.item(), "time:",(time.time()-start).seconds)


torch.save(generator.state_dict(), 'models/generator.pth')
torch.save(discriminator.state_dict(), 'models/discriminator.pth')