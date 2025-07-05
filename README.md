# CSC361-WebTester.py (HTTP and HTTPS Analyzer)

## Overview

**WebTester** is a Python program designed to connect to a web server, analyze HTTP/HTTPS responses, and collect key information such as:

- Supported protocol versions (e.g., whether HTTP/2 is supported)
- List of cookies set by the server
- Security status (whether the site is password-protected or not)

This tool provides a lightweight way to assess basic HTTP response behavior and cookie data from any publicly available web server.

---

## How to Run

1. **Unzip** the submitted folder.
2. **Open Terminal** and navigate to the directory containing `WebTester.py`.
3. Run the following command:

```bash
python3 WebTester.py <url>
```

Replace `<url>` with any valid URL. For example:

```bash
python3 WebTester.py www.uvic.ca
```

---

## Input Examples

```bash
python3 WebTester.py www.uvic.ca
python3 WebTester.py uvic.ca
python3 WebTester.py https://www.uvic.ca
python3 WebTester.py www.youtube.com
python3 WebTester.py www.netflix.com
```

### Error Examples (Invalid Input)

```bash
python3 WebTester.py www.
python3 WebTester.py
```

### Example with a Password-Protected Page (401 Unauthorized)

```bash
python3 WebTester.py https://docs.engr.uvic.ca/docs/
```

---

## Output Example

```text
---Request begin---
GET www.uvic.ca HTTP/1.1
Host: www.uvic.ca
Connection: Keep-Alive

---Request end---

HTTP request sent, awaiting response...

302
https://www.uvic.ca/

200
---Response Header---
HTTP/1.1 200 OK
Date: Fri, 27 Sep 2024 22:21:12 GMT
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Set-Cookie: PHPSESSID=7o9v0mjc93cvo7fgleshq2l2nr; path=/; secure; HttpOnly; SameSite=Lax
Set-Cookie: uvic_bar=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/; domain=.uvic.ca; secure; HttpOnly
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Vary: Accept-Encoding,User-Agent
Feature-Policy: accelerometer 'none'; camera 'none'; geolocation 'none'; gyroscope 'none'; magnetometer 'none'; microphone 'none'; payment 'none'; usb 'none'
Connection: close
Content-Type: text/html; charset=UTF-8
Set-Cookie: www_def=!Tk720JzoXGFgy192WoCbqs3+3m8im6nuFZkYzVd8QS8Ohy7qG7efCDDVGVHbrPpiijNPYNHUOCkQvEU=; path=/; Httponly; Secure
Strict-Transport-Security: max-age=16070400
Set-Cookie: TS018b3cbd=0183e0753443eefdc62258187626db7661ffa7a78acd98768f713e085b8cff9a59ca17d19cbff447544971c76f7e82f42cc8cda17c291a9a9e6699822b40257cec9363bafde40a1a10aefecb8b1389a5d6ece51b18; Path=/; Secure; HTTPOnly
Set-Cookie: TS0165a077=0183e0753487e943502f73f16988b6b47daa5aaf4ecd98768f713e085b8cff9a59ca17d19c622923a1c3bb6424febe1252802b9beed6a9ae2c53d7a8f4c4d2ade0ee255378; path=/; domain=.uvic.ca; HTTPonly; Secure

website: www.uvic.ca
1. Supports http2: no
2. List of Cookies:
   - cookie name: PHPSESSID
   - cookie name: uvic_bar, expires time: Thu, 01-Jan-1970 00:00:01 GMT, domain name: .uvic.ca
   - cookie name: www_def
   - cookie name: TS018b3cbd
   - cookie name: TS0165a077, domain name: .uvic.ca
3. Password-protected: no
```

---

## Author

Developed as part of **CSC361 - Computer Communications and Networking** coursework.

---


