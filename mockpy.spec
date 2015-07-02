# -*- mode: python -*-
import site
import os
block_cipher = None

def check_path_exists(path):
  if not os.path.exists(path):
    print("Required path `%s` missing" % path)
    exit(0)

a = Analysis(['mockpy.py'],
             pathex=['/Users/omarsubhiabdelhafith/Documents/Python/mockpy/mockpy'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)

a.datas += [("sample.yml", "mockpy/data/sample.yml", "DATA" )]

path = site.getsitepackages()[0] + "/cryptography/hazmat/bindings/openssl/src"
check_path_exists(path)

a.datas += Tree(
    path,
    prefix = "cryptography/hazmat/bindings/openssl/src"
)

path = "../mitmproxy/libmproxy/onboarding/templates"
check_path_exists(path)

a.datas += Tree(
  path,
  prefix="libmproxy/onboarding/templates"
)

path = "../mitmproxy/libmproxy/onboarding/static"
check_path_exists(path)

a.datas += Tree(
  path,
  prefix="libmproxy/onboarding/static"
)

pyz = PYZ(a.pure,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='mockpy',
          debug=False,
          strip=None,
          upx=True,
          console=True )
