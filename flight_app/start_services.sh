#!/bin/bash

# Check if model.pkl is older than 10 days
MODEL_FILE="backend/model.pkl"
if [ ! -f "$MODEL_FILE" ] || [ $(( (`date +%s` - `stat -L -c %Y $MODEL_FILE`) / 86400 )) -gt 10 ]; then
    echo "Model is older than 10 days or doesn't exist. Retraining..."
    cd model
    python train_model.py
    cd ..
    echo "Model retrained successfully!"
fi

echo "Stopping any existing services..."
lsof -ti:5000,8000 | xargs kill -9 2>/dev/null || true

echo "Starting backend service..."
cd backend
python app.py &
BACKEND_PID=$!

echo "Starting frontend service..."
cd ../client
python app.py &
FRONTEND_PID=$!

echo "Services started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend running on http://localhost:5000"
echo "Frontend running on http://localhost:8000"

# Wait for both processes
wait