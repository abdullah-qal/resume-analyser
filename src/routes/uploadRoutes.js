const express = require('express');
const upload = require('../config/multerConfig');
const { handleFileUpload } = require('../controllers/uploadController');

const router = express.Router();

router.post('/upload', upload.single('file'), handleFileUpload);

module.exports = router;