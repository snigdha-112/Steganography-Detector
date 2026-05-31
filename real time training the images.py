import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import cv2
import numpy as np
import os

class StegoDataset(Dataset):
    def __init__(self, clean_dir, stego_dir, size=256):
        self.size = size
        self.samples = []
        for f in os.listdir(clean_dir):
            c = os.path.join(clean_dir, f)
            s = os.path.join(stego_dir, f.replace(".jpg", ".png"))
            if os.path.exists(s):
                self.samples.append((c, 0))
                self.samples.append((s, 1))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = cv2.imread(path, 0)
        img = cv2.resize(img, (self.size, self.size))
        tensor = torch.from_numpy(img).unsqueeze(0).float() / 255.0
        return tensor, torch.tensor([float(label)])

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
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return torch.sigmoid(self.fc2(x))

dataset = StegoDataset("D:/stegoproject/dataset/clean",
                       "D:/stegoproject/dataset/stego")

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_set, val_set = torch.utils.data.random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_set, batch_size=16, shuffle=True)
val_loader = DataLoader(val_set, batch_size=16, shuffle=False)

print(f"Training: {len(train_set)} samples | Validation: {len(val_set)} samples")

model = StegoCNN()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

NUM_EPOCHS = 20
print("Training Started")

for epoch in range(NUM_EPOCHS):
    model.train()
    train_loss = 0
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()

    model.eval()
    val_loss, correct, total = 0, 0, 0
    with torch.no_grad():
        for images, labels in val_loader:
            outputs = model(images)
            val_loss += criterion(outputs, labels).item()
            predicted = (outputs > 0.5).float()
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

    acc = 100 * correct / total
    print(f"Epoch {epoch+1}/{NUM_EPOCHS} | Train Loss: {train_loss/len(train_loader):.4f} | Val Loss: {val_loss/len(val_loader):.4f} | Accuracy: {acc:.1f}%")

torch.save(model.state_dict(), "D:/stegoproject/stego_cnn.pth")
print("Model saved to D:/stegoproject/stego_cnn.pth")
print("Training Complete!")
