# -*- mode: python -*-

block_cipher = None


a = Analysis(['autochat.py'],
             pathex=['C:\\Users\\�ż���\\Desktop\\p1\\Autochat'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='autochat',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='Wechat.ico')
