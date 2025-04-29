const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const express = require('express');
const path = require('path');
const multer = require('multer');
const qrcode = require('qrcode-terminal');
const db = require('./db'); // Import the database module

const app = express();
const PORT = process.env.PORT || 3000;

const upload = multer({ dest: 'uploads/' });

const client = new Client({
    authStrategy: new LocalAuth()
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
    console.log('QR Code generated! Scan it using your WhatsApp.');
});

client.on('ready', () => {
    console.log('WhatsApp Client is ready!');
    
    // Automatically resume sending pending messages when the client is ready
    db.getPendingMessages((messages) => {
        if (messages.length > 0) {
            console.log('Resuming pending messages...');
            messages.forEach(async (message) => {
                if (message.status === 'pending') {
                    await client.sendMessage(message.number + "@c.us", message.message);
                    db.updateMessageStatus(message.id, 'sent');
                }
            });
        }
    });
});

let stopRequested = false;

app.post('/stop', (req, res) => {
    stopRequested = true;
    res.send('Sending stopped successfully.');
});

app.post('/send', upload.array('files'), async (req, res) => {
    const number = req.body.number;
    const messages = req.body.messages.split('\n');
    const speed = parseInt(req.body.speed) || 1000;
    const files = req.files;

    if (!number || !messages.length) {
        return res.status(400).send('Number and messages are required.');
    }

    const chatId = number + "@c.us";

    try {
        stopRequested = false;

        for (let message of messages) {
            if (stopRequested) break;

            // Add message to queue (persistent)
            db.addMessageToQueue(number, message);

            await client.sendMessage(chatId, message);
            console.log(`Sent message: ${message}`);
            await new Promise(resolve => setTimeout(resolve, speed));
        }

        if (files && files.length > 0 && !stopRequested) {
            for (let file of files) {
                const media = MessageMedia.fromFilePath(file.path);
                await client.sendMessage(chatId, media);
                console.log(`Sent file: ${file.originalname}`);
                await new Promise(resolve => setTimeout(resolve, speed));
            }
        }

        if (stopRequested) {
            res.send('Sending stopped by user.');
        } else {
            res.send('Messages and files sent successfully!');
        }

    } catch (error) {
        console.error('Error sending message:', error);
        res.status(500).send('Error: ' + error);
    }
});

client.initialize();

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
