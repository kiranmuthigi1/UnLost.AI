const express = require("express");
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');
const lost = require('./../models/losts.js');
const { exec } = require('child_process');

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, new Date().toISOString().replace(/:/g, '-') + file.originalname);
    }
});

const fileFilter = (req, file, cb) => {
    // reject a file
    if (file.mimetype === 'image/jpeg' || file.mimetype === 'image/png' || file.mimetype === 'image/jpg') {
        cb(null, true);
    } else {
        cb(null, false);
    }
};

const upload = multer({
    storage: storage,
    limits: {
        fileSize: 1024 * 1024 * 50
    },
    fileFilter: fileFilter
});

async function rearrangeFiles(labelname, files) {
    fs.mkdirSync(`lostdb/${labelname}`, {recursive: true, mode: 770});
    await files.forEach((file, i) => {
        // exec(`mv ${file.path} lostdb/${labelname}/${i}.${path.extname(file.originalname)}`);
        fs.renameSync(`${file.path}`, `lostdb/${labelname}/${i}.${path.extname(file.originalname)}`);
    });
    
    // console.log('stdout:', stdout);
    // console.log('stderr:', stderr);
  }


router.post('/uploadlost', upload.array("lostImage", 10), (req, res, next) => {
    if(req.files.size<=0 ) {
        res.status(500).json({
            status: "fail"
        });
    } else {
        const mongooseId = mongoose.Types.ObjectId();
        const labelname = mongooseId;
        
        const newimage = new lost({
            _id: mongooseId,
            label: labelname,

        });

        
        rearrangeFiles(labelname, req.files);

        newimage
            .save()
            .then((result) => {
                console.log(result);
                res.status(200).json({
                    status: "success"
                });
            }).catch(err => {
                console.log(err);
                res.status(500).json({
                    status: "fail"
                });            
            });

        /**
         * Delete files from Uploads folder after it has been moved to lostdb folder
         * req.files.forEach((file, i) => {
            fs.unlink(`${file.path}`, (err) => {
                if (err) throw err;
                console.log(`${file.path} was deleted`);
            });
            });
         */
        
    }
    
});

module.exports = router;