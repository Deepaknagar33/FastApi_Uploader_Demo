import os
from typing import List, Dict, Any
from fastapi import UploadFile


# this is the project demo name API

def _sanitize_relpath(relpath: str) -> str:
    """
    Sanitize a relative path from the client (webkitRelativePath).
    - Normalizes separators.
    - Disallows absolute paths, drive letters, and path traversal.
    """
    norm = os.path.normpath(relpath).replace("\\", "/")  # normalize separators
    while norm.startswith("./") or norm.startswith("/"):
        norm = norm[2:] if norm.startswith("./") else norm[1:]
    if not norm or norm.startswith("../") or "/../" in norm or norm == "..":
        raise ValueError(f"Unsafe path component: {relpath!r}")
    if ":" in os.path.splitdrive(norm)[0]:
        raise ValueError(f"Unsafe drive path: {relpath!r}")
    return norm

async def _save_streamed(file: UploadFile, dest_path: str) -> int:
    """Stream the uploaded file to disk to avoid loading it fully in memory."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    size = 0
    chunk_size = 1024 * 1024  # 1 MB
    await file.seek(0)
    with open(dest_path, "wb") as out:
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            out.write(chunk)
            size += len(chunk)
    return size

async def save_uploaded_files(
    files: List[UploadFile],
    upload_root: str = "app/uploads",
    excluded_exts: List[str] = None
) -> Dict[str, Any]:
    """
    Saves multiple uploaded files under `upload_root`, keeping folder structure.
    Skips extensions provided in `excluded_exts`.

    Args:
        files: list of UploadFile objects from FastAPI.
        upload_root: base folder to save files into.
        excluded_exts: list of extensions (e.g., [".pdf", ".exe"]) to skip.

    Returns summary dict: { total, saved, skipped, errors, message }.
    """
    excluded_exts = {ext.lower() for ext in (excluded_exts or [])}
    saved, skipped, errors = [], [], []
    os.makedirs(upload_root, exist_ok=True)

    for uf in files:
        try:
            relpath = _sanitize_relpath(uf.filename or os.path.basename(uf.filename))
        except Exception as e:
            errors.append({"file": uf.filename, "reason": str(e)})
            continue

        ext = os.path.splitext(relpath)[1].lower()

        if ext in excluded_exts:
            skipped.append(relpath)
            await uf.read()  # drain the stream
            continue

        dest_path = os.path.join(upload_root, relpath.replace("/", os.sep))
        try:
            written = await _save_streamed(uf, dest_path)
            saved.append({"path": relpath, "bytes": written})
        except Exception as e:
            errors.append({"file": relpath, "reason": str(e)})

    msg = f"Saved {len(saved)} file(s), skipped {len(skipped)} ({', '.join(sorted(excluded_exts)) or 'none'})"
    if errors:
        msg += f", errors {len(errors)}"

    return {
        "total": len(files),
        "saved": saved,
        "skipped": skipped,
        "errors": errors,
        "message": msg,
    }
