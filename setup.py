from setuptools import setup

APP = ['main.py']
DATA_FILES = ['practice.json']
OPTIONS = {
    'argv_emulation': True,
    # 'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'Coaching Practice Finance',
        'CFBundleDisplayName': 'Coaching Practice Finance',
        'CFBundleGetInfoString': "Coaching Practice Finance",
        'CFBundleIdentifier': "com.example.coaching-practice-finance",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
