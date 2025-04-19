#!/bin/bash

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