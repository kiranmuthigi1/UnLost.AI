const mongoose = require('mongoose');

const foundSchema = mongoose.Schema({
    _id : mongoose.Schema.Types.ObjectId,
    label: { type: String },
    email: { type: String },
    timestamp: {type: Data, default: Date.now}
});

module.exports = mongoose.model('Founds', foundSchema);