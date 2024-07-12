import requests
import concurrent.futures
import time

def send_request(session, url, method='GET', data=None):
    if method == 'GET':
        response = session.get(url)
    elif method == 'POST':
        response = session.post(url, json=data)
    elif method == 'PUT':
        response = session.put(url, json=data)
    elif method == 'DELETE':
        response = session.delete(url)
    else:
        return None
    return response.status_code

def main():
    url = "http://127.0.0.1:5000"
    num_requests = 10000000  # 요청수
    max_workers = 1000  # 최대 동시 실행 쓰레드 수

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        with requests.Session() as session:
            futures = [executor.submit(send_request, session, url) for _ in range(num_requests)]
            for future in concurrent.futures.as_completed(futures):
                try:
                    status = future.result()
                    if status != 200:
                        print(f"Request failed with status code: {status}")
                except Exception as e:
                    print(f"Request failed: {e}")
    
    end_time = time.time()
    print(f"All requests completed in {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
