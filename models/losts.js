const mongoose = require('mongoose');

const lostSchema = mongoose.Schema({
    _id : mongoose.Schema.Types.ObjectId,
    label: { type: String },
    // images: [String]
});

module.exports = mongoose.model('Losts', lostSchema);