# -*- mode: python -*-

block_cipher = None


a = Analysis(['mockpy.py'],
             pathex=['/Users/omarsubhiabdelhafith/Documents/Python/mockpy/mockpy'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)

a.datas += [("sample.yml", "mockpy/data/sample.yml", "DATA" )]

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
