import os

# Set up proxy environment variables if needed
#os.environ['HTTP_PROXY'] = 'http://user:password@host:8080'
#os.environ['HTTPS_PROXY'] = 'http://user:password@host:8080'

proxies = {
    'http': os.environ.get('HTTP_PROXY'),
    'https': os.environ.get('HTTPS_PROXY')
}


os.environ['GITHUB_URL'] = "shihuan99/shihuan99.github.io" if os.environ.get('GITHUB_URL') is None else os.environ['GITHUB_URL']
os.environ['GITHUB_START_PATH'] = "docs/kafka" if os.environ.get('GITHUB_START_PATH') is None else os.environ['GITHUB_START_PATH']
os.environ['GITHUB_BRANCH'] = "main" if os.environ.get('GITHUB_BRANCH') is None else os.environ['GITHUB_BRANCH']

# os.environ['BASE_URL'] = "https://api.siliconflow.cn/v1"
# os.environ['API_KEY'] = "Your Api Key Here"