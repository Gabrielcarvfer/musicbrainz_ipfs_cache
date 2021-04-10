from flask import Flask, request
import requests
import hashlib
import os
from threading import Lock
import time

app = Flask("MusicBrainz IPFS Cache")

cache_directory_path = "ipfs"
mb_address = "musicbrainz.org"
mb_port = "443"
mb_request_path = "https://"+mb_address+":"+mb_port
mb_rate_limiter_lock = Lock()
mb_rate = 1  # requests per second


def sha1(content):
    sha_calc = hashlib.sha1()
    sha_calc.update(content.encode("utf-8"))
    return sha_calc.hexdigest()


@app.route('/ws/2/<path:req>')
def cacheable_requests(req):
    req_path = request.full_path

    # calculate hash of the requested path
    sha = sha1(req_path)
    cached_filename = "ipfs/%s.json" % sha

    # check if entry is cached
    if os.path.exists(cached_filename):
        with open(cached_filename, "rb") as file:
            contents = file.read()
        return contents, 200
    else:
        # Prevents more than a single request per second
        with mb_rate_limiter_lock:
            time.sleep(1.0/mb_rate)

        mb_response = requests.get(mb_request_path+req_path+"&fmt=json")

        # MB responded the value existed
        if mb_response.status_code == 200:
            with open(cached_filename, "wb") as file:
                file.write(mb_response.content)
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

    # Prevents more than a single request per second
    with mb_rate_limiter_lock:
        time.sleep(1.0 / mb_rate)

    mb_response = requests.get(mb_request_path+req_path)
    return mb_response.content, mb_response.status_code


if __name__ == '__main__':
    if not os.path.exists(cache_directory_path):
        os.mkdir(cache_directory_path)
    app.run(port=80)