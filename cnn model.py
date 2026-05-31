
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import cv2
import numpy as np

# --- MODEL ---
class StegoCNN(nn.Module):
    def __init__(self):
        super(StegoCNN, self).__init__()
        
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.pool = nn.AvgPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)

        self.fc1 = nn.Linear(64 * 64 * 64, 128)
        self.fc2 = nn.Linear(128, 1)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        
        x = x.view(x.size(0), -1)   # ✅ FIXED
        
        x = F.relu(self.fc1(x))
        return torch.sigmoid(self.fc2(x))


# --- CREATE MODEL ---
model = StegoCNN()
print("Success! The Stego-Detective Brain has been built.")

# --- TRAINING SETUP ---
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# --- TRAIN FUNCTION ---
def train_one_step(image_data, true_label):
    
    model.train()   # ✅ important
    
    optimizer.zero_grad()
    
    guess = model(image_data)
    
    true_label = true_label.float().view(-1, 1)   # ✅ FIXED
    
    loss = criterion(guess, true_label)
    
    loss.backward()
    optimizer.step()
    
    print(f"Loss: {loss.item()}")


# --- LOAD IMAGES ---
clean_img = cv2.imread("D:/stegoproject/flower.jpg", 0)
stego_img = cv2.imread("D:/stegoproject/stego_flower.png", 0)

# ✅ IMPORTANT FIX: resize
clean_img = cv2.resize(clean_img, (256, 256))
stego_img = cv2.resize(stego_img, (256, 256))

# --- SRM FILTER ---
srm_filter = np.array([[-1, 2, -1], [2, -4, 2], [-1, 2, -1]])

c_noise = cv2.filter2D(clean_img, -1, srm_filter)
s_noise = cv2.filter2D(stego_img, -1, srm_filter)

# --- TO TENSOR ---
c_tensor = torch.from_numpy(c_noise).unsqueeze(0).unsqueeze(0).float() / 255.0
s_tensor = torch.from_numpy(s_noise).unsqueeze(0).unsqueeze(0).float() / 255.0

# --- LABELS ---
clean_label = torch.tensor([[0.0]])
stego_label = torch.tensor([[1.0]])

# --- TRAIN ---
print("\n--- Starting Training ---")

for epoch in range(10):
    train_one_step(c_tensor, clean_label)
    train_one_step(s_tensor, stego_label)
    
    print(f"Round {epoch+1} complete\n")

print("Training Finished!")
