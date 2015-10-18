# -*- mode: python -*-
a = Analysis(['baboon.py'],
             pathex=['/Users/guoxin/DropboxNU/Dropbox/My Research/Code/Python/baboon'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + [('baboon1.png','baboon1.png','DATA'),('baboon2.png','baboon2.png','DATA')],
          name='baboon',
          debug=False,
          strip=None,
          upx=True,
          console=True )
if sys.platform == 'darwin':
            app = BUNDLE(exe, name='baboon.app', icon=None)
         
