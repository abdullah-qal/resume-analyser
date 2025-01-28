const multer = require('multer');
const path = require('path');

const uploadsDir = path.join(__dirname, '../../uploads');

const fileStorageEngine = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadsDir);
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '--' + file.originalname);
    }
});

const upload = multer({ storage: fileStorageEngine });

module.exports = upload;