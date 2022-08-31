# Minidump Upload Example

An example tool that uploads minidumps and event payloads to Sentry with
compression built with the Sentry Python SDK.

## Installation

It is recommended to install dependencies in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

To upload a minidump, export the `SENTRY_DSN` environment variable and call it
with the path to the file. This will compress the minidump before sending it to
Sentry:

```bash
export SENTRY_DSN="..."
./upload.py /path/to/mini.dmp
```

The script prints out the event ID of a new error event that will be created
through the upload.

The script takes an optional event payload JSON as second parameter. The JSON
file can be downloaded from the _Issue Details_ page. This is useful when
additional context and breadcrumb information from the original minidump
submission should also be reuploaded.

```bash
export SENTRY_DSN="..."
./upload.py /path/to/mini.dmp /path/to/event.json
```
