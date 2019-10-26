const express = require("express");
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');
const lost = require('./../models/losts.js');
const found = require('./../models/found.js');

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'temp/');
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

async function rearrangeFiles(labelname, files, category) {
    fs.mkdirSync(`uploads/${category}/${labelname}`, {recursive: true, mode: 770});

    await files.forEach((file, i) => {
        fs.renameSync(`${file.path}`, `uploads/${category}/${labelname}/${i}.${path.extname(file.originalname)}`);
    });
    
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

        
        rearrangeFiles(labelname, req.files, 'lost');

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

router.post('/uploadfound', upload.array("foundImage", 10), (req, res, next) => {
    if(req.files.size<=0 ) {
        res.status(500).json({
            status: "fail"
        });
    } else {
        const mongooseId = mongoose.Types.ObjectId();
        const labelname = mongooseId;
        
        const newfimage = new found({
            _id: mongooseId,
            label: labelname

        });

        
        rearrangeFiles(labelname, req.files, 'found');

        newfimage
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
        
    }
});


module.exports = router;