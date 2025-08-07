import torch
import torch.nn as nn
import torch.optim as optim

X = torch.randn(100, 1)
y = 2 * X + 1 + torch.randn(100, 1) * 0.1

model = nn.Linear(1, 1)

criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

epochs = 1000
for epoch in range(epochs):
    outputs = model(X)
    loss = criterion(outputs, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

predicted = model(torch.tensor([[2.0]]))
print(f'Prediction for input 2.0: {predicted.item():.4f}')