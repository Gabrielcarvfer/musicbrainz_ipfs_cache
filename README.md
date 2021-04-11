1. Download the IPFS CLI in: https://dist.ipfs.io/#go-ipfs
2. Run `ipfs init` to configure the node
3. Run `ipfs daemon` to run the deamon
4. Clone the repo, install requirements and execute the main.py
    - 4.1 ipfshttpclient doesn't officialy support ipfs 0.8.0, but changing the version checking works just fine
5. Point MusicBrainz Picard to the server address and port running main.py
6. The server will do one of these   
    - 6.1 If there is no cached metadata, forward request to MusicBrainz API, cache it and forward answer to Picard
    - 6.2 If there is cached metadata, answer Picard directly