import torch
import torch.nn as nn
import torch.nn.init as init
import pandas as pd
import joblib

def predict_churn(df:pd.DataFrame):
    scaler = joblib.load("Outputs/Models/scaler.pkl")

    X_scaler = scaler.transform(df)

    X_tensor = torch.tensor(X_scaler, dtype=torch.float32)

    model = ChurnNN(input_dim=X_tensor.shape[1], hidden_dim=64, output_dim=1, activation=nn.ReLU(), dropout_rate=0.3)

    model.load_state_dict(torch.load("Outputs/Models/churn_model.pth"))
    model.eval()

    with torch.no_grad():
        y_pred = model(X_tensor)
        pred_probs = y_pred.squeeze().numpy()
        pred_label = (pred_probs > 0.5).astype(int)

    return pred_probs, pred_label

class ChurnNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, activation, dropout_rate):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, hidden_dim)
        self.fc4 = nn.Linear(hidden_dim, output_dim)

        self.activation = activation
        self.dropout = nn.Dropout(dropout_rate)

        for layer in [self.fc1, self.fc2, self.fc3, self.fc4]:
            init.kaiming_uniform_(layer.weight, nonlinearity='relu')
            init.zeros_(layer.bias)

    def forward(self, x):
        x = self.activation(self.fc1(x))
        x = self.dropout(x)
        x = self.activation(self.fc2(x))
        x = self.dropout(x)
        x = self.activation(self.fc3(x))
        x = torch.sigmoid(self.fc4(x))

        return x
