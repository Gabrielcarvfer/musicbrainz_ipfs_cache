from flask import Flask, request
import requests
import hashlib

app = Flask("MusicBrainz IPFS P2P Cache Client")
app_port = 81

mb_address = "localhost"  # Change this the real IPFS cache server ip+port
mb_port = "80"
mb_request_path = "http://"+mb_address+":"+mb_port

ipfsGateway = "https://cloudflare-ipfs.com/ipfs/"
ipfsServerPeerId = "12D3KooWCrhd7hrEx9aW8jXB5ZJaiJZZTEeyDquKK8jNPvugKrru"
# IPFS cache server folder hash will be resolved with IPNS pointing to the Peer ID
ipfsServerHash = "QmTVbx4D4s9HYhX2edW6YM1Z5EqFe8cLUsZE8z1P7qqqWD"
ipfsClient = None


def sha1(content):
    sha_calc = hashlib.sha1()
    sha_calc.update(content.encode("utf-8"))
    return sha_calc.hexdigest()


@app.route('/ws/2/<path:req>')
def cacheable_requests(req):
    req_path = request.full_path

    # calculate hash of the requested path
    sha = sha1(req_path)
    cached_filename = "%s/%s.json" % (ipfsServerHash, sha)

    # check if entry is cached on the gateway
    found = False
    try:
        ipfs_response = ipfsClient.pin.add(cached_filename)
        if ipfs_response:
            found = True
    except Exception:
        pass

    if found:
        # if the entry exists, it got pinned to the local client and will be shared amongst other peers
        return ipfsClient.cat(cached_filename), 200
    else:
        # if it doesn't, forward the request to the MusicBrainz IPFS Cache server
        mb_response = requests.get(mb_request_path+req_path)

        # if it answers positively, try to pin the response to share amongst other peers
        if mb_response.status_code == 200:
            try:
                ipfsClient.pin.add(cached_filename)
            except Exception:
                pass
        return mb_response.content, mb_response.status_code


@app.route("/oauth2/<path:req>")
def oauth_requests(req):
    # non_cacheable_requests(request.full_path) # authentication is broken
    return {}, 400


@app.route("/static/<path:req>")
def static_requests(req):
    non_cacheable_requests(request.full_path)


def non_cacheable_requests(req_path):
    # If not /ws/2/ api, we act as a man-in-the-middle and forward requests to MB
    # (OK for proof-of-concept, disturbing for production)
    mb_response = requests.get(mb_request_path+req_path)
    return mb_response.content, mb_response.status_code


if __name__ == '__main__':
    # Create IFPS client to talk with deamon
    import ipfshttpclient

    ipfsClient = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001")

    try:
        # Resolve IPFS server hash with IPNS
        ipnsServerHash = ipfsClient.name.resolve(ipfsServerPeerId)
        ipnsServerHash = ipfsServerHash.get("Path").split('/')[-1]
        ipfsServerHash = ipnsServerHash
    except Exception:
        print("Failed to resolve IPFS server hash. Falling back to IPFS folder hash.")

    # Start cache server
    app.run(port=app_port)