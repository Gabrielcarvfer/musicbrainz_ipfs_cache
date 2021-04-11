WARNING
=======
This is just a proof-of-concept. Not ready for production.

Server (a.k.a. MusicBrainz Server's sidekick)
===================

1. Download the IPFS CLI in: https://dist.ipfs.io/#go-ipfs
2. Run `ipfs init` to configure the node
3. Run `ipfs daemon` to run the daemon
4. Clone the repo, install requirements and execute the `server.py`
    - 4.1 ipfshttpclient doesn't officially support ipfs 0.8.0, but changing the version checking works just fine
5. Point MusicBrainz Picard to the server address and port running `server.py`
6. The server will do one of these   
    - 6.1 If there is no cached metadata, forward request to MusicBrainz API, cache it and forward answer to Picard
    - 6.2 If there is cached metadata, answer Picard directly
   
Client-side (a.k.a. Picard's sidekick)
==================
1. Point out the "MB server" address/port (not the real one, but the sidekick) and the IPFS folder hash
2. Run `client.py` (you don't need the IPFS client to do that)
3. Point Picard to the local address and port and let it do its magic