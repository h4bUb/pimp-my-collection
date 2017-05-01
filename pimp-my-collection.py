from pimper.pimper import Pimper


src = r""
dst = r""
chromedriver_location = ""
pimper = Pimper(src, dst, chromedriver_location, fast_proxy=True)
pimper.pimp()