const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

// read the JSON data from file
async function readJsonData(filePath) {
  return new Promise((resolve, reject) => {
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) {
        reject(err);
        return;
      }
      resolve(JSON.parse(data));
    });
  });
}

async function updateKV() {
  // Path to the JSON file
  const jsonFilePath = path.join(__dirname, '..', '..', 'item-info-generator', 'item_data.json');

  try {
    const data = await readJsonData(jsonFilePath);
    const value = JSON.stringify(data);

    // key to store the JSON data in KV
    const key = "item_data";

    const url = `https://api.cloudflare.com/client/v4/accounts/${process.env.CF_ACCOUNT_ID}/storage/kv/namespaces/${process.env.CF_NAMESPACE_ID}/values/${key}`;
    
    const response = await axios.put(url, value, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.CF_API_TOKEN}`,
        "Content-Length": Buffer.byteLength(value)
      }
    });

    console.log('KV updated successfully:', response.data);
  } catch (error) {
    console.error('Error updating KV:', error);
  }
}

updateKV();