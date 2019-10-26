const mongoose = require('mongoose');

const foundSchema = mongoose.Schema({
    _id : mongoose.Schema.Types.ObjectId,
    label: { type: String },
});

module.exports = mongoose.model('Founds', foundSchema);