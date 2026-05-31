import torch
import torch.nn as nn
import torch.optim as optim

# 1. Choose the 'Grader' (Loss Function)
criterion = nn.BCEWithLogitsLoss()   # safer than BCELoss

# 2. Choose the 'Coach' (Optimizer)
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 3. TRAINING LOOP
def train_one_step(image_data, true_label):
    
    model.train()  # set training mode
    
    optimizer.zero_grad()
    
    # Brain makes a guess
    guess = model(image_data)
    
    # Fix label shape + type
    true_label = true_label.float().view(-1, 1)
    
    # Grader checks the guess
    loss = criterion(guess, true_label)
    
    # Brain learns from the mistake
    loss.backward()
    optimizer.step()
    
    print(f"Training Step Complete. Loss (Error Score): {loss.item()}")
