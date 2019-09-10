const mongoose = require('mongoose')

const schema = new mongoose.Schema({
    title: { type: String },
    body: { type: String },
    icon: { type: String }
    // category: {}
}, {
    timestamps: true
})

module.exports = mongoose.model('Article', schema)