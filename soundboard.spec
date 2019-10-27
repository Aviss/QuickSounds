# -*- mode: python -*-

# Build script to compile into exe. Requires "PyInstaller". Call "pyinstaller soundboard.spec" from the commandline

block_cipher = None

a = Analysis(['QuickSounds.py'],
             binaries=[
				(HOMEPATH + "\\_sounddevice_data\\portaudio-binaries\\libportaudio64bit.dll", "_sounddevice_data\\portaudio-binaries"),
				(HOMEPATH + "\\_soundfile_data\\libsndfile64bit.dll", "_soundfile_data")
			 ],
             datas=[
				("resources", "resources"),
				("cfg.ini", ".")
			 ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['_ssl', '_hashlib', 'unicodedata', '_distutils_findvs', '_multiprocessing', '_win32sysloader', '_bz2', '_lzma', '_decimal',
					   'win32com.shell.shell', 'win32pdh', 'win32trace', 'win32ui', 'win32wnet',
					   'numpy.core.multiarray_tests',
					   'PIL._webp'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
			 
a.binaries = a.binaries - TOC([
	('mfc140u.dll', None, 'BINARY'),
	('ucrtbase.dll', None, 'BINARY')
])

a.binaries = [x for x in a.binaries if not x[0].startswith("api-ms-win")]
			 
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='QuickSounds',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='soundboard')
