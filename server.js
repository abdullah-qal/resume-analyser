const express = require('express');
const app = express();

const multer = require('multer');

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

app.post('/upload', upload.single('file'), (req, res) => {
    console.log(req.file);
    res.send('Single file uploaded');
});
app.listen(3000);