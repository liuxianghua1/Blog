module.exports = app => {
    const express = require('express')
    const router = express.Router()
    const Category = require('../../model/category')

    router.post('/category', async (req, res) => {
        const model = await Category.create(req.body)
        res.send(model)
    })

    router.get('/category', async (req, res) => {
        const category = await Category.find()
        res.send(category)
    })

    router.get('/category/:id', async (req, res) => {
        const category = await Category.findById(req.params.id)
        res.send(category)
    })

    router.put('/category/:id', async (req, res) => {
        const category = await Category.findByIdAndUpdate(req.params.id, req.body)
        res.send(category)
    })

    router.delete('/category/delete/:id', async (req, res) => {
        const category = await Category.findByIdAndDelete(req.params.id)
        res.send(category)
    })

    app.use('/admin/api', router)
}