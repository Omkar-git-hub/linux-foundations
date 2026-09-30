"""
Notes module for common networking command-line tools and concepts:
- curl
- wget
- ports
- DNS

Each function returns a formatted string containing concise reference
information that can be used in documentation, tutorials, or REPL
sessions.
"""

def curl_notes() -> str:
    """
    Return a quick reference guide for ``curl`` usage.

    Highlights:
    - Basic GET request
    - POST request with data
    - Saving output to a file
    - Following redirects
    - Using custom headers
    - Verbose / silent modes
    - TLS/SSL options
    """
    return (
        "curl (Client URL) – command‑line tool for transferring data with URLs.\n"
        "\n"
        "Common options:\n"
        "  -X <METHOD>          Specify request method (GET, POST, PUT, DELETE …)\n"
        "  -d <DATA>            Send POST data (application/x-www-form-urlencoded)\n"
        "  -F <NAME=CONTENT>    Send multipart/form‑data (file upload)\n"
        "  -H <HEADER>          Add custom header (e.g., \"Authorization: Bearer …\")\n"
        "  -o <FILE>            Write output to <FILE> (instead of stdout)\n"
        "  -O                   Save remote file with its original name\n"
        "  -L                   Follow redirects (HTTP 3xx)\n"
        "  -I                   Fetch only the HTTP headers (HEAD request)\n"
        "  -u <USER:PASS>       Basic authentication\n"
        "  -k / --insecure      Allow insecure SSL connections\n"
        "  -s / --silent        Silent mode (no progress meter or error messages)\n"
        "  -v / --verbose       Verbose output (includes request/response headers)\n"
        "\n"
        "Examples:\n"
        "  curl https://example.com                     # simple GET\n"
        "  curl -L http://short.url                     # follow redirects\n"
        "  curl -o page.html https://example.com        # save to file\n"
        "  curl -O https://example.com/file.tar.gz      # keep remote filename\n"
        "  curl -d \"name=John&age=30\" -X POST \\\n"
        "       https://api.example.com/users          # POST form data\n"
        "  curl -H \"Accept: application/json\" \\\n"
        "       https://api.example.com/items          # custom header\n"
        "  curl -u user:pass https://secure.example.com # basic auth\n"
    )

def wget_notes() -> str:
    """
    Return a quick reference guide for ``wget`` usage.

    Highlights:
    - Simple file download
    - Recursive mirroring
    - Resuming downloads
    - Limiting download speed
    - Using proxies
    - HTTPS/TLS options
    """
    return (
        "wget – non‑interactive network downloader.\n"
        "\n"
        "Common options:\n"
        "  -O <FILE>            Write output to <FILE> (default is remote name)\n"
        "  -c / --continue     Resume partially downloaded files\n"
        "  -r / --recursive    Download recursively (mirroring)\n"
        "  -l <DEPTH>          Set recursion maximum depth (default 5)\n"
        "  -np / --no-parent   Do not ascend to parent directories\n"
        "  -A <LIST>           Accept only files matching the comma‑separated list\n"
        "  -R <LIST>           Reject files matching the list\n"
        "  --limit-rate=<RATE> Limit download speed (e.g., 200k, 2m)\n"
        "  --user=<USER> --password=<PASS>  HTTP authentication\n"
        "  --proxy=on|off      Enable/disable proxy usage\n"
        "  --no-check-certificate  Skip SSL certificate verification\n"
        "  -q / --quiet        Quiet output (no progress bar)\n"
        "  -nv / --no-verbose  Less verbose output (no headers)\n"
        "\n"
        "Examples:\n"
        "  wget https://example.com/file.zip               # simple download\n"
        "  wget -c https://example.com/large.iso           # resume download\n"
        "  wget -r -np -nH --cut-dirs=1 -R \"index.html*\" \\\n"
        "       https://example.com/docs/                 # mirror a directory\n"
        "  wget --limit-rate=500k https://example.com/video.mp4\n"
        "  wget --no-check-certificate https://self-signed.example.com/\n"
    )

def ports_notes() -> str:
    """
    Return a concise reference about TCP/UDP ports, common utilities,
    and typical usage patterns.
    """
    return (
        "Ports – 16‑bit numbers (0‑65535) identifying a specific service on a host.\n"
        "\n"
        "Ranges:\n"
        "  0‑1023   Well‑known ports (assigned by IANA, e.g., 80 HTTP, 443 HTTPS)\n"
        "  1024‑49151  Registered ports (assigned to applications, e.g., 3306 MySQL)\n"
        "  49152‑65535 Dynamic/private ports (ephemeral, used for client connections)\n"
        "\n"
        "Common utilities:\n"
        "  netstat -tuln          List listening sockets (requires sudo for all)\n"
        "  ss -tulnp              Modern replacement for netstat\n"
        "  lsof -iTCP -sTCP:LISTEN   Show processes listening on TCP ports\n"
        "  nmap -p 1-65535 <host>    Scan all ports on a host\n"
        "  nc (netcat) -zv <host> <port>   Test connectivity to a single port\n"
        "\n"
        "Typical tasks:\n"
        "  • Identify which process owns a port:\n"
        "        sudo lsof -i :8080\n"
        "  • Open a firewall rule (iptables example):\n"
        "        sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT\n"
        "  • Temporarily forward a local port to a remote service (ssh):\n"
        "        ssh -L 8080:remote.host:80 user@remote.host\n"
    )

def dns_notes() -> str:
    """
    Return a quick reference guide for DNS concepts and common command‑line tools.
    """
    return (
        "DNS – Domain Name System, translating human‑readable hostnames to IP addresses.\n"
        "\n"
        "Key record types:\n"
        "  A      IPv4 address record\n"
        "  AAAA   IPv6 address record\n"
        "  CNAME  Canonical name (alias)\n"
        "  MX     Mail exchange server\n"
        "  TXT    Arbitrary text (often used for SPF, DKIM)\n"
        "  NS     Authoritative name server\n"
        "  PTR    Reverse lookup (IP → hostname)\n"
        "\n"
        "Common command‑line tools:\n"
        "  dig [@server] name [type]   Perform DNS queries (default A)\n"
        "  host name [server]          Simple lookup utility\n"
        "  nslookup name [server]      Interactive query tool (legacy)\n"
        "  drill name [type]           Lightweight DNS lookup (part of ldns)\n"
        "\n"
        "Examples:\n"
        "  dig example.com                     # basic A record lookup\n"
        "  dig MX example.com +short           # list mail exchangers\n"
        "  dig +trace example.com              # follow the delegation chain\n"
        "  dig @8.8.8.8 example.com AAAA        # query Google DNS for IPv6 address\n"
        "  host -t TXT _spf.google.com         # retrieve SPF record\n"
        "\n"
        "Useful flags:\n"
        "  +short   Show concise answer only\n"
        "  +noall +answer   Show only answer section\n"
        "  +tcp    Use TCP for the query (default UDP)\n"
        "  +retry=<N>   Number of retries before giving up\n"
    )