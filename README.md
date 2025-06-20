# 🌸 5chan CLI: Own the Signal

## 📋 What is this tool all about?
<strong>Peer-powered. No middlemen. No mercy.</strong>

♔ Spin up your own server — you're the host, you're the firewall, you're the last line.
Messages are end-to-end encrypted using a shared symmetric key, because trust isn’t outsourced.⛓

♔ You and your peer share the key. No key, no decrypt. Just silence.

♔ No key? No problem — fall back to plaintext and whisper into the void like it’s 1999.

<strong>Welcome to 5chan. Speak freely, but bring your own cipher.🕵️</strong>

<hr>

## 😼How to dig in ?
- Clone the repo  
  Because nothing screams *“trust me bro”* like downloading code from the internet.

- To host the server, run the `server.py` file.  
  Bonus: Host it on AWS EC2, a shady VPS, or your cousin's Raspberry Pi duct-taped to a modem — your server, your problem.

- Want encryption? Generate a symmetric key.  
  That’s right, the **same key** on both ends.

- Share that key with your peer. Yes, *share it*.  
  Whisper it over the phone, carve it into a tree, tattoo it under your eyelid — just don’t post it on Discord.  
  When launching `client.py`, enter the server address *and* the key.  
  If the key matches, chat is encrypted. If not, it’s plaintext — raw and vulnerable, like your browsing history.

- No key?  
  Then it’s bare-knuckle comms, baby. Unencrypted. Untamed. Just like the early internet intended.


## Join the 5chan Chat Collective (LIMITED Edition)

Yeah, it’s limited — blame the AWS Free Tier overlords.  
This server’s not trying to be Signal, Tor, or Skynet.  
It's a **demo**, a **playground**, a **test lab with a pulse**.

Ghost mode enabled 👻  
Use it, break it, meme on it — just don’t expect 99.99% uptime or quantum resistance.

- Here's the server address: <span style="color:red">54.210.191.138</span>  
- Port: 1060  

<strong>Seriously, don’t be that person — this server is for community fun and testing, not target practice.</strong>

## Usage and Screenshots

### 🖥️ Spin up the Server
  
- Fire up ```server.py``` like a true gigachad. This bad boy waits for clients to yeet themselves into the chatroom.

  
![Screenshot 2025-06-20 181234](https://github.com/user-attachments/assets/8c48b1fe-8e6c-4fac-8721-e90027cadc67)

### 👥 Client Joins the Fray

- Run client.py on another terminal (or summon your friends if you’re not socially bankrupt). Boom—you’re connected.

![Screenshot 2025-06-20 181218](https://github.com/user-attachments/assets/0c822e3d-f698-4e57-91b6-df6777521c55)



