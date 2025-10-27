def set_timer(root, attr_name, delay_ms, callback, target):
    """Crée un timer Tkinter et stocke son identifiant."""
    tid = root.after(delay_ms, callback)
    setattr(target, attr_name, tid)


def cancel_timer(root, attr_name, target):
    """Annule un timer Tkinter stocké dans une instance."""
    tid = getattr(target, attr_name, None)
    if tid is not None:
        try:
            root.after_cancel(tid)
        except Exception:
            pass
        setattr(target, attr_name, None)
