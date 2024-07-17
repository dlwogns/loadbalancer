import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import concurrent.futures
import time

def send_request(session, url, method='GET', data=None):
    if method == 'GET':
        response = session.get(url, timeout=5)
    elif method == 'POST':
        response = session.post(url, json=data, timeout=5)
    elif method == 'PUT':
        response = session.put(url, json=data, timeout=5)
    elif method == 'DELETE':
        response = session.delete(url, timeout=5)
    else:
        return None
    return response.status_code

def main():
    url = "http://127.0.0.1:5000/test"
    num_requests = 10000  # 요청수
    max_workers = 100
    # 최대 동시 실행 쓰레드 수
    # 흠 이걸 어떻게 해야될까

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        with requests.Session() as session:
            adapter = HTTPAdapter(
                pool_connections=100,  # 풀 연결 수 설정
                pool_maxsize=100,      # 최대 풀 크기 설정
                max_retries=Retry(total=3, backoff_factor=0.1),  # 재시도 설정 (선택 사항)
            )
            session.mount("http://", adapter)
            futures = [executor.submit(send_request, session, url) for _ in range(num_requests)]
            for future in concurrent.futures.as_completed(futures):
                try:
                    status = future.result()
                    if status != 200:
                        #print(f"Request failed with status code: {status}")
                        pass
                except Exception as e:
                    print(f"Request failed: {e}")
    
    end_time = time.time()
    print(f"All requests completed in {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
