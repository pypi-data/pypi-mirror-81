class IOBase:
    def seek(self, pos, whence=0): ...
    def tell(self): ...
    def truncate(self, pos=None): ...
    def flush(self): ...
    def close(self): ...
    def seekable(self): ...
    def readable(self): ...
    def writable(self): ...
    @property
    def closed(self): ...
    def __enter__(self): ...
    def __exit__(self, *args): ...
    def fileno(self): ...
    def isatty(self): ...
    def readline(self, size=-1): ...
    def readlines(self, hint=None): ...
    def writelines(self, lines): ...


class RawIOBase(IOBase):
    def read(self, size=-1): ...
    def readall(self): ...
    def readinto(self, b): ...
    def write(self, b): ...


class BufferedIOBase(IOBase):
    def read(self, size=-1): ...
    def read1(self, size=-1): ...
    def readinto(self, b): ...
    def readinto1(self, b): ...
    def write(self, b): ...
    def detach(self): ...


class TextIOBase(IOBase):
    def read(self, size=-1): ...
    def write(self, s): ...
    def truncate(self, pos=None): ...
    def readline(self): ...
    def detach(self): ...
    @property
    def encoding(self): ...
    @property
    def newlines(self): ...
    @property
    def errors(self): ...
