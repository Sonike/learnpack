# How the internet works

## Why this matters

As a backend engineer you'll write programs that other computers talk to over a network. When something breaks ("the site is down", "the API times out", "it works on my machine but not on the server"), you need a mental picture of what actually happens between a click and a page. Is it DNS? The wrong port? HTTPS? This lesson gives you that picture. It's also a classic interview question: "what happens when you type a URL into the browser and press Enter?"

## 1. Clients and servers

Nearly everything on the web follows one pattern:

- A **client** asks for something. Your browser, a phone app, or a Python script.
- A **server** answers. A program running on a computer somewhere, waiting for requests.

```
  client                              server
+---------+   "give me /products"   +---------+
| browser | ----------------------> | web app |
|         | <---------------------- |         |
+---------+   "here's the page"     +---------+
```

"Server" means two things, and people use both: the **program** that answers requests, and the **computer** it runs on. A single computer can run many server programs, and in the next sections you'll write one.

The client always starts the conversation. A server can't call your browser out of the blue; it can only answer.

## 2. IP addresses and ports

To send a message to a computer, you need its address. On the internet that's an **IP address** (Internet Protocol address):

```
IPv4:  142.250.187.206
IPv6:  2a00:1450:4009:81f::200e
```

IPv4 addresses are four numbers from 0 to 255. There are only about 4 billion of them, which isn't enough, so the longer IPv6 format exists too. You'll see both.

One computer runs many programs, so an address alone isn't enough. A **port** is a number from 0 to 65535 that says *which program* on that computer should get the message. Think of the IP address as a building's street address and the port as the flat number.

Some ports are conventions everyone follows:

| Port | Used for |
|---|---|
| 80 | HTTP (plain web traffic) |
| 443 | HTTPS (encrypted web traffic) |
| 22 | SSH (logging into a remote machine) |
| 5432 | PostgreSQL |
| 8000, 8080, 3000 | common choices for development servers |

When you type `https://example.com`, your browser uses port 443 automatically because the scheme is `https`. You only write a port when it isn't the default: `http://localhost:8000`.

## 3. localhost

There's a special address that always means "this computer": **`localhost`**, which is the IP address `127.0.0.1`. When you run a web server on your laptop during development, you visit it at something like `http://localhost:8000`. The request never leaves your machine. If a colleague types `localhost:8000` on *their* laptop, they reach *their* machine, not yours. This trips people up more than you'd think.

## 4. Packets and routing

Data doesn't travel as one big piece. It's split into small chunks called **packets**, each a few hundred to about 1,500 bytes, and each labelled with the source and destination IP addresses.

Packets hop through many **routers** (computers that forward packets towards their destination) on the way. Different packets from the same message may take different routes and arrive out of order, or not at all.

```
your laptop -> home router -> ISP -> ... -> data centre -> server
               (each hop just forwards packets one step closer)
```

You can see the hops yourself:

```bash
traceroute example.com      # tracert example.com on Windows
```

```
 1  192.168.1.1 (192.168.1.1)  2.1 ms
 2  10.20.0.1 (10.20.0.1)  9.8 ms
 ...
 9  93.184.215.14 (93.184.215.14)  88.2 ms
```

## 5. TCP and UDP

If packets can arrive out of order or get lost, how does a web page arrive intact? A protocol on top of IP handles it. A **protocol** is just an agreed set of rules for a conversation.

- **TCP** (Transmission Control Protocol) makes a reliable connection. It numbers packets, puts them back in order, and re-sends any that get lost. Before data flows, client and server do a quick "handshake" to set up the connection. The web, email and databases use TCP.
- **UDP** (User Datagram Protocol) just fires packets off with no guarantees. It's faster and simpler, which suits video calls and games, where a late packet is useless anyway.

You'll almost always be on TCP. The useful takeaway: setting up a connection takes a round trip or two, which is why keeping connections open and reusing them makes things faster.

## 6. DNS: names to numbers

Humans remember `github.com`, not `140.82.121.4`. **DNS** (the Domain Name System) is the internet's phone book: you give it a **domain name**, it gives you back an **IP address**.

```bash
nslookup example.com
```

```
Name:    example.com
Address: 93.184.215.14
```

Behind the scenes your computer asks a **DNS resolver** (usually run by your internet provider, or a public one like Cloudflare's `1.1.1.1`), which asks other DNS servers until it finds the answer. Answers are **cached** (kept for a while) at every step, so most lookups are instant.

DNS is a common culprit when things break: "the site is down" sometimes means "the domain's DNS record is wrong or expired", and after you change a DNS record, old answers can linger in caches for minutes or hours.

## 7. URLs: the address of a resource

A **URL** (Uniform Resource Locator) says exactly where something is and how to get it. Every part has a job:

```
https://shop.example.com:8443/products/42?colour=red&size=m#reviews
\___/   \______________/ \__/ \_________/ \_______________/ \_____/
scheme       host        port    path          query       fragment
```

- **scheme**: which protocol to use, usually `http` or `https`.
- **host**: the domain name (or an IP address) of the server.
- **port**: optional. If it's missing, use the default for the scheme: 80 for `http`, 443 for `https`.
- **path**: which resource on that server. `/` if empty.
- **query**: extra parameters after `?`, as `key=value` pairs joined by `&`.
- **fragment**: after `#`, a position inside the page. The browser keeps this to itself; it is **never sent to the server**.

Python can split a URL for you:

```python
from urllib.parse import urlsplit, parse_qs

parts = urlsplit("https://shop.example.com:8443/products/42?colour=red&size=m#reviews")
print(parts.scheme, parts.hostname, parts.port, parts.path)
# https shop.example.com 8443 /products/42
print(parts.query, parse_qs(parts.query))
# colour=red&size=m {'colour': ['red'], 'size': ['m']}
print(parts.fragment)
# reviews
```

In the practice exercise you'll write this yourself with string methods, to see there's no magic in it.

## 8. HTTPS: why the padlock matters

**HTTP** (HyperText Transfer Protocol) is the language browsers and web servers speak; the next lesson, *HTTP in depth*, is all about it. Plain HTTP is sent as readable text. Anyone between you and the server (the café's Wi-Fi, a compromised router) can read it, including passwords, and even change it.

**HTTPS** is HTTP sent through **TLS** (Transport Layer Security), which gives you three things:

1. **Encryption**: people in the middle see scrambled bytes.
2. **Integrity**: if anyone changes the data in transit, it's detected.
3. **Authentication**: the server proves it really is `bank.example.com` with a **certificate** signed by an authority your browser trusts.

Every site should use HTTPS, and every API you build should only be reachable over HTTPS in production. Hosting platforms, which you'll deploy to later in the course, set it up for you.

## 9. Putting it together: what happens when you press Enter

You type `https://example.com/about` and press Enter:

```
1. Parse the URL      scheme=https, host=example.com, port=443, path=/about
2. DNS lookup         example.com  ->  93.184.215.14
3. TCP connection     handshake with 93.184.215.14 on port 443
4. TLS handshake      check the certificate, agree on encryption keys
5. HTTP request       GET /about  (sent encrypted)
6. Server works       routes /about to some code, maybe queries a database
7. HTTP response      200 OK + the HTML for the page
8. Render             the browser draws the page, then repeats 5-7 for
                      each image, stylesheet and script it references
```

Each step is a place things can go wrong, and each has a different symptom:

| Symptom | Likely step |
|---|---|
| "Server not found" / `Name or service not known` | 2, DNS |
| "Connection refused" | 3, nothing is listening on that port (is your server running?) |
| "Your connection is not private" | 4, a certificate problem |
| A 404 or 500 page | 6–7: you reached the server, and it answered with an error |

## Common mistakes

**Assuming `localhost` is shared.** Your `localhost` is your machine only. To let someone else reach your development server, you need a real address.

**`Connection refused` on `localhost:8000`.** Nothing is listening there. The server isn't running, crashed at start-up, or is on a different port. Read the server's start-up output for the port it actually chose.

**Thinking the fragment reaches the server.** `/page#section-2` sends just `/page`. If your backend needs a value, it must be in the path or query.

**Forgetting default ports.** `https://example.com` and `https://example.com:443` are the same address. `http://example.com:443` is not: it speaks plain HTTP to a port expecting TLS, and fails.

**Sending secrets over plain HTTP.** Passwords and API keys must only ever travel over HTTPS.

## Recap

- Clients ask, servers answer, and the client always starts.
- An **IP address** finds the computer, a **port** finds the program on it. `localhost` (127.0.0.1) is your own machine.
- Data travels as **packets** through routers; **TCP** makes that reliable, **UDP** trades reliability for speed.
- **DNS** turns names into IP addresses, and caches the answers.
- A **URL** is scheme, host, port (default 80/443), path, query and fragment; the fragment never reaches the server.
- **HTTPS** = HTTP over TLS: encrypted, tamper-evident, and the server proves who it is.
- Loading a page: URL → DNS → TCP → TLS → HTTP request → server → response → render.
