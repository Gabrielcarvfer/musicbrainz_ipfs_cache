from flask import Flask, request
import requests
import hashlib

app = Flask("MusicBrainz IPFS Gateway Cache Client")
app_port = 81

mb_address = "localhost"  # Change this the real IPFS cache server ip+port
mb_port = "80"
mb_request_path = "http://"+mb_address+":"+mb_port

ipfsGateway = "https://cloudflare-ipfs.com/ipfs/"
ipfsServerHash = "QmTVbx4D4s9HYhX2edW6YM1Z5EqFe8cLUsZE8z1P7qqqWD"  # Change this the real IPFS cache server folder hash
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
    ipfs_response = requests.get(ipfsGateway+cached_filename)
    if ipfs_response.status_code == 200:
        return ipfs_response.content, 200
    else:
        # if it isn't, forward the request to the MusicBrainz IPFS Cache server
        mb_response = requests.get(mb_request_path+req_path)
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
    # Start cache server
    app.run(port=app_port)