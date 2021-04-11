WARNING
=======
This is just a proof-of-concept. Not ready for production.

Setup
=======
1. Download the IPFS CLI in: https://dist.ipfs.io/#go-ipfs
2. Run `ipfs init` to configure the node
3. Run `ipfs daemon` to run the daemon
4. Clone the repo, install requirements
    - 4.1 ipfshttpclient doesn't officially support ipfs 0.8.0, but changing the version checking works just fine

Server (a.k.a. MusicBrainz Server's sidekick)
=============================================
5. Configure the target MB server and local server ip+port.
6. Point MusicBrainz Picard to the server address and port running `server.py`
7. The server will do one of these   
    - 7.1 If there is no cached metadata, forward request to MusicBrainz API, cache it and forward answer to Picard
    - 7.2 If there is cached metadata, answer Picard directly
   
Client-side (a.k.a. Picard's sidekick)
======================================
5. Point out the "MB server" address/port (not the real one, but the sidekick) and the IPFS folder hash
6. Choose one to run:
   - 6.1 Dumb client: `gateway-client.py` (you <b>DON'T NEED</b> the IPFS client to do that)
   - 6.2 P2P client: `p2p-client.py` (you <b>NEED</b> the IPFS client to do that)
7. Point Picard to the local client address and port and let it do its magic
