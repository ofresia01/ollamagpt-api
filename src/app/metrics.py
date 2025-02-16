from prometheus_client import Counter, Gauge

ollama_requests_total = Counter('ollama_requests_total', 'Total number of requests to Ollama')
ollama_errors_total = Counter('ollama_errors_total', 'Total number of errors from Ollama')
ollama_response_time = Gauge('ollama_response_time', 'Response time of Ollama requests')