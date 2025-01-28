const express = require('express');
const path = require('path');
const fs = require('fs');
const uploadRoutes = require('./routes/uploadRoutes');

const app = express();

// Create the uploads directory if it doesn't exist
const uploadsDir = path.join(__dirname, '../uploads');
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
}

// Serve static files from the public folder
app.use(express.static(path.join(__dirname, '../public')));

// Use the upload routes
app.use('/', uploadRoutes);

// Start the server
app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});