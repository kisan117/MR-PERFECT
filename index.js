
const { Client, LocalAuth } = require('whatsapp-web.js');
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;
const qrcode = require('qrcode-terminal');

const client = new Client({
    authStrategy: new LocalAuth()
});

client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
    console.log('QR Code स्कैन कीजिए।');
});

client.on('ready', () => {
    console.log('WhatsApp Client तैयार है!');
});

app.use(express.json());

app.post('/send', async (req, res) => {
    const number = req.body.number;
    const message = req.body.message;

    if (!number || !message) {
        return res.status(400).send('Number और Message दोनों चाहिए।');
    }

    const chatId = number + "@c.us";
    try {
        await client.sendMessage(chatId, message);
        res.send('Message भेज दिया गया।');
    } catch (error) {
        res.status(500).send('Error: ' + error);
    }
});

app.listen(PORT, () => {
    console.log(`Server चालू है Port: ${PORT}`);
});

client.initialize();
