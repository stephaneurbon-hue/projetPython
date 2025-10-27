"""
Fonctions utilitaires pour la gestion des timers Tkinter
"""

def set_timer(root, name, delay, callback, obj):
    tid = root.after(delay, callback)
    setattr(obj, name, tid)

def cancel_timer(root, name, obj):
    tid = getattr(obj, name, None)
    if tid:
        try:
            root.after_cancel(tid)
        except Exception:
            pass
        setattr(obj, name, None)
