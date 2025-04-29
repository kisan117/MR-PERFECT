const express = require('express');
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Multer config for file uploads
const upload = multer({ dest: 'uploads/' });

// Create WhatsApp client
const client = new Client({
    authStrategy: new LocalAuth()
});

// Static file serving
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

// Variables to store QR Code
let qrCodeImage = '';

// Serve frontend HTML
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Serve QR code as Image
app.get('/qr', async (req, res) => {
    if (qrCodeImage) {
        res.send(qrCodeImage);
    } else {
        res.send('QR Code not generated yet, refresh in few seconds.');
    }
});

// WhatsApp client events
client.on('qr', async (qr) => {
    qrCodeImage = await qrcode.toDataURL(qr);
    console.log('QR code updated, please scan.');
});

client.on('ready', () => {
    console.log('WhatsApp Client is ready!');
});

// POST route to send message and media
app.post('/send', upload.array('files'), async (req, res) => {
    const number = req.body.number;
    const messages = req.body.messages.split('\n');
    const files = req.files;

    if (!number || !messages || messages.length === 0) {
        return res.status(400).send('Both number and messages are required.');
    }

    const chatId = number + '@c.us';

    try {
        for (let message of messages) {
            await client.sendMessage(chatId, message);
        }

        if (files && files.length > 0) {
            for (let file of files) {
                const media = MessageMedia.fromFilePath(file.path);
                await client.sendMessage(chatId, media);
                fs.unlinkSync(file.path); // File delete after sending
            }
        }

        res.send('Messages and files sent successfully!');
    } catch (error) {
        res.status(500).send('Error sending message: ' + error);
    }
});

// Initialize WhatsApp client
client.initialize();

// Start server
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
