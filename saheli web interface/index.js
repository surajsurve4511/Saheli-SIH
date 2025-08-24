const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const server = http.createServer(app); // Create an HTTP server
const wss = new WebSocket.Server({ server }); // Attach WebSocket to the server

// Serve static files from the 'public' directory
app.use(express.static('public'));

// WebSocket connection logic
wss.on('connection', (ws) => {
  console.log('New WebSocket connection');

  ws.on('message', (message) => {
    console.log('Received:', message);
  });

  
});

// Handle HTTP requests (e.g., your REST API or serving your React app)
app.get('/api', (req, res) => {
  res.json({ message: 'Hello from the server!' });
});

// Start the server on port 3000
const PORT = 5000;
server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
