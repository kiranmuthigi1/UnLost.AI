const mongoose = require('mongoose');

const lostSchema = mongoose.Schema({
    _id : mongoose.Schema.Types.ObjectId,
    label: { type: String },
    isEncoding: {type: Boolean, default: false}
});

module.exports = mongoose.model('Losts', lostSchema);
