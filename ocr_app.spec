# ocr_app.spec
block_cipher = None

a = Analysis(
    ['ocr.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Tesseract-OCR/*', 'Tesseract-OCR'),
        ('Tesseract-OCR/tessdata/*.traineddata', 'Tesseract-OCR/tessdata'),
        ('NotoSerifEthiopic-Bold.ttf', '.'),
        ('habesha.json', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='HabeshaOCR',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='HabeshaOCR'
)
