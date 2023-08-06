# servo-webhooks
![Run Tests](https://github.com/opsani/servo-webhooks/workflows/Run%20Tests/badge.svg)
[![license](https://img.shields.io/github/license/opsani/servo-webhooks.svg)](https://github.com/opsani/servo-webhooks/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/servo-webhooks.svg)](https://pypi.org/project/servo-webhooks/)
[![release](https://img.shields.io/github/release/opsani/servo-webhooks.svg)](https://github.com/opsani/servo-webhooks/releases/latest)
[![GitHub release date](https://img.shields.io/github/release-date/opsani/servo-webhooks.svg)](https://github.com/opsani/servo-webhooks/releases)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=opsani/servo-webhooks)](https://dependabot.com)

An Opsani [Servo](https://github.com/opsani/servox) connector that provides a flexible webhooks 
emitter based on [servo events](https://github.com/opsani/servox/#understanding-events).

The webhooks connector extends the eventing infrastruture provided by the servo to enable events 
to be dispatched via HTTP or HTTP/2 request callbacks. Requests are delivered asynchronously on a 
best effort basis. Webhooks can be registered to execute *before* or *after* any event defined in 
the servo assembly. Before event webhooks should be used with care as they can block execution of the
event pending delivery of the webhook or cancel the event entirely through the response (see below).
Support is provided for configurable automatic retry and timeout of webhook requests.

Webhook requests are sent with the HTTP `POST` method and a JSON request body. The webhook request body 
is dynamically defined based on the parameters and return value of the event registered with the servo. 
This mechanism generalizes the webhook connector to support arbitrary events defined by any connector 
within the servo assembly. The `Content-Type` header and request body JSON Schema can be obtained 
via the `webhooks` CLI subcommand (see usage below).

## Configuration

```yaml
webhooks:
  - name: my_measure_handler # Optional. Name of the webhook.    
    description: Store measurement info into Elastic Search. # Optional: Textual description of the webhook
    events:
    - after:measure # Required. Format: `(before|after):[EVENT_NAME]`
    url: https://example.com/webhooks # Required. Format: [URL]
    secret: s3cr3t # Required. Secret value for computing webhook signatures
    headers: # Optional, Dict[str, str]
      - name: x-some-header
        value: some value
    backoff: # Optional. Setting to `false` disables retries.
      max_tries: 3
      max_time: 5m
```

A starting point configuration can be added to your servo assembly via: `servo generate --defaults webhooks`.

## Example Webhook Requests

# TODO: Insert headers and request body for a couple of events
```console
```

## Installation

servo-webhooks is distributed as an installable Python package via PyPi and can be added to a servo assembly via Poetry:

```console
❯ poetry add servo-webhooks
```

For convenience, servo-webhooks is included in the default servox assembly [Docker images](https://hub.docker.com/repository/docker/opsani/servox).

## Usage

1. Listing webhooks: `servo webhooks list`
1. Getting event content type and payload schema: `servo webhooks schema after:measure`
1. Triggering an ad-hoc webhook: `servo webhooks trigger after:adjust ([NAME|URL])`

### Implementing Webhook Responders

TODO: Content type, etc. headers. Include connector version, other event metadata. Schema versioning.

### Validating Webhook Signatures

All webhook requests are sent with a `X-Servo-Signature` header. This value of this header is a hex
string representation of an HMAC SHA1 digest computed over the body of the request using the value of 
the `secret` key from the webhook configuration. The signature can be easily verified to validate the 
authenticity and integrity of the webhook payload. HMAC computation is supported on all major platforms
and in the standard library of most modern programming languages.

An example of computing an HMAC SHA1 digest from a webhook request in Python looks like this:

```python
secret = "super secret authentication code"
expected_signature = request.headers["x-servo-signature"]
body = request.read()
signature = str(hmac.new(secret.encode(), body, hashlib.sha1).hexdigest())
assert signature == expected_signature
```


### Cancelling an Event via a Webhook

Let's say that you want to implement a webhook that implements authorization of adjustments based on criteria 
such as a schedule that only permits them during midnight and 3am. To implement this, the webhook responder will
return a 200 (OK) status code and a response body modeling a `servo.errors.CancelEventError` object. The `servo-webhooks`
connector will deserialize the `CancelEventError` representation and raise a `CancelEventError` exception within the
assembly, cancelling the event. To indicate that your response body is a representation of a `CancelEventError` error,
set the `Content-Type` header to `application/vnd.opsani.servo.errors.CancelEventError+json` and return a JSON object 
that includes a `reason` property describing why the event was cancelled:
TODO: What's the best status code/response for cancellation?
Return a 200 (OK) response with `Content-Type` of :

```
> POST http://webhooks.example.com/servo-webhooks
> Content-Type: application/vnd.opsani.servo.events.Event+json # TODO: Not the right content type
> {
>  ...
> }

< 200 (OK)
< Content-Type: application/vnd.opsani.servo.errors.CancelEventError+json
< {
<  "reason": "Unable to authorize adjustment: Adjustments are only permitted between midnight and 3am."
< }
```

### Configuring Backoff Retries & Timeouts

TODO: Disabling backoff to avoid blocking on a before handler.

## Technical Details

Webhook requests are managed non-persistently in memory. Requests are made via an asynchronous [httpx](https://www.python-httpx.org/) 
client built on top of [asyncio](https://asyncio.readthedocs.io/). Support for webhook request body JSON Schema is provided via the 
deep integration of [Pydantic](https://pydantic-docs.helpmanual.io/) in servox. Backoff and retry supported is provided via the 
[backoff](https://pypi.org/project/backoff/) library.

## Testing

Automated tests are implemented via [Pytest](https://docs.pytest.org/en/stable/): `pytest test_servo_webhooks.py`

## License

servo-webhooks is distributed under the terms of the Apache 2.0 Open Source license.

A copy of the license is provided in the [LICENSE](LICENSE) file at the root of the repository.
