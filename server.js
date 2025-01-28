const express = require('express');
const app = express();
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const pdfParse = require('pdf-parse');


const uploadsDir = path.join(__dirname, 'uploads');

// Create the uploads directory if it doesn't exist
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
}

const fileStorageEngine = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, './uploads')
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '--' + file.originalname)
    }
})
const upload = multer({ storage: fileStorageEngine });

app.use(express.static('public'));

// Handle file uploads
app.post('/upload', upload.single('file'), async (req, res) => {
    try {
        // Check if a file was uploaded
        if (!req.file) {
            return res.status(400).send('No file uploaded.');
        }

        // Check if the uploaded file is a PDF
        if (req.file.mimetype !== 'application/pdf') {
            return res.status(400).send('Only PDF files are allowed.');
        }

        // Read the uploaded PDF file
        const dataBuffer = fs.readFileSync(req.file.path);

        // Extract text from the PDF
        const data = await pdfParse(dataBuffer);

        // Log the extracted text
        console.log('Extracted Text:', data.text);

        // Send the extracted text as a response
        res.send(`<h1>Extracted Text:</h1><pre>${data.text}</pre>`);
    } catch (error) {
        console.error('Error processing PDF:', error);
        res.status(500).send('An error occurred while processing the PDF.');
    }
});

app.listen(3000);