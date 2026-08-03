# Demo memory

This folder contains a sample `remembrandt` memory store so you can inspect
exactly what a real store looks like without setting anything up.

```bash
# Inspect the store
remembrandt --dir examples/demo/.remembrandt recall
remembrandt --dir examples/demo/.remembrandt status
```

The compiled human-readable memory lives in
[`.remembrandt/MEMORY.md`](.remembrandt/MEMORY.md).

Rebuild it anytime with:

```bash
make demo-data
```
