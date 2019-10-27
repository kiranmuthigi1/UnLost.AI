const mongoose = require('mongoose');

const lostSchema = mongoose.Schema({
    _id : mongoose.Schema.Types.ObjectId,
    label: { type: String },
    isEncoding: {type: Boolean, default: false},
    email: {type: String},
    timestamp: {type: Date, default: Date.now}
});

module.exports = mongoose.model('Losts', lostSchema);
