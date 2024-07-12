from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def backend(path):
    request_count += 1
    return jsonify({"message": f"Handled by {request.host}", "method": request.method, "path": path, "request_cnt": request_count})

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])
    global request_count
    request_count = 0
    app.run(port=port)