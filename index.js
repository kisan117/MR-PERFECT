const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode'); // यह QR code इमेज जनरेट करने में मदद करेगा
const app = express();

// WhatsApp क्लाइंट इनिशियलाइज करें
const client = new Client({
    authStrategy: new LocalAuth()
});

app.use(express.static('public')); // स्टैटिक फाइल्स सर्व करने के लिए (QR Code इमेज डिस्प्ले के लिए)

// HTML पेज सर्व करने का रूट
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// QR कोड जनरेट करें और फ्रंटएंड पर भेजें
client.on('qr', (qr) => {
    qrcode.toDataURL(qr, (err, url) => {
        if (err) {
            console.log("QR जनरेट करते समय त्रुटि:", err);
        }
        // QR कोड इमेज URL फ्रंटएंड पर भेजें
        res.send(`<img src="${url}" alt="Scan this QR Code with WhatsApp">`);
    });
});

// जब क्लाइंट तैयार हो जाए
client.on('ready', () => {
    console.log('WhatsApp क्लाइंट तैयार है!');
});

// WhatsApp क्लाइंट इनिशियलाइज करें
client.initialize();

// Express सर्वर शुरू करें
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`सर्वर पोर्ट ${PORT} पर चल रहा है`);
});
