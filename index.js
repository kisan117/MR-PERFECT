const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const express = require('express');
const path = require('path');
const multer = require('multer');  // To handle file uploads
const qrcode = require('qrcode'); // QR code module added
const fs = require('fs'); // To handle file operations

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize multer for file upload handling
const upload = multer({ dest: 'uploads/' });

// Create a new client for WhatsApp
const client = new Client({
    authStrategy: new LocalAuth()
});

// Serve the HTML form at the root endpoint
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Generate QR code dynamically and serve to the user
client.on('qr', async (qr) => {
    // Generate QR code and save it as an image file
    await qrcode.toFile('./qr-code.png', qr, function (err) {
        if (err) console.error('Error generating QR code:', err);
        console.log('QR Code saved to qr-code.png');
    });
    console.log('QR Code generated! Scan it in WhatsApp Web.');
});

// Serve the generated QR code as an image
app.get('/qr-code', (req, res) => {
    res.sendFile(path.join(__dirname, 'qr-code.png'));
});

// When the client is ready
client.on('ready', () => {
    console.log('WhatsApp Client is ready!');
});

// Route to send messages and files
app.post('/send', upload.array('files'), async (req, res) => {
    const number = req.body.number;
    const messages = req.body.messages.split('\n'); // Split messages by new line
    const files = req.files;  // Handle uploaded files

    if (!number || !messages || messages.length === 0) {
        return res.status(400).send('Both number and messages are required.');
    }

    const chatId = number + "@c.us";

    try {
        // Send multiple messages
        for (let message of messages) {
            await client.sendMessage(chatId, message);
        }

        // Send files if any
        if (files && files.length > 0) {
            for (let file of files) {
                const media = MessageMedia.fromFilePath(file.path);
                await client.sendMessage(chatId, media);
            }
        }

        res.send('Messages and files sent successfully!');
    } catch (error) {
        res.status(500).send('Error: ' + error);
    }
});

// Initialize the WhatsApp client
client.initialize();

// Start the Express server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
