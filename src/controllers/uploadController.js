const parsePdf = require('../utils/pdfParser');

const handleFileUpload = async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).send('No file uploaded.');
        }

        if (req.file.mimetype !== 'application/pdf') {
            return res.status(400).send('Only PDF files are allowed.');
        }

        const extractedText = await parsePdf(req.file.path);
        res.send(`<h1>Extracted Text:</h1><pre>${extractedText}</pre>`);
    } catch (error) {
        console.error('Error processing file:', error);
        res.status(500).send('An error occurred while processing the file.');
    }
};

module.exports = { handleFileUpload };