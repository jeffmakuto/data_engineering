import traceback

try:
    import app
    print('imported app module, has attribute app:', hasattr(app, 'app'))
    print('module dir:', dir(app))
except Exception:
    traceback.print_exc()
