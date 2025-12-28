class BaseLogger:
    def info(self, message): pass
    def error(self, message): pass

class StreamlitLogger(BaseLogger):
    def __init__(self, log_func):
        self.log_func = log_func
    
    def info(self, message):
        self.log_func(f"ℹ️ {message}")
        
    def error(self, message):
        self.log_func(f"❌ {message}")