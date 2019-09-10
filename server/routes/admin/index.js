module.exports = app => {
    const express = require('express')
    const router = express.Router({
        mergeParams: true
    })

    router.post('/', async (req, res) => {
        const Model = require(`../../model/${req.params.resource}`)
        const model = await Model.create(req.body)
        res.send(model)
    })

    router.get('/', async (req, res) => {
        const Model = require(`../../model/${req.params.resource}`)
        const category = await Model.find()
        res.send(category)
    })

    router.get('/:id', async (req, res) => {
        const Model = require(`../../model/${req.params.resource}`)
        const category = await Model.findById(req.params.id)
        res.send(category)
    })

    router.put('/:id', async (req, res) => {
        const Model = require(`../../model/${req.params.resource}`)
        const category = await Model.findByIdAndUpdate(req.params.id, req.body)
        res.send(category)
    })

    router.delete('/delete/:id', async (req, res) => {
        const Model = require(`../../model/${req.params.resource}`)
        const category = await Model.findByIdAndDelete(req.params.id)
        res.send(category)
    })

    app.use('/admin/api/rest/:resource', router)

    const multer = require('multer')
    const upload = multer({dest: __dirname + '/../../uploads'})
    app.post('/admin/api/upload',upload.single('file'), async(req, res) => {
            const file = req.file;
            file.url = `http://localhost:3000/uploads/${file.filename}`
            res.send(file)
    })
}