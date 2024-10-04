from microdot import Microdot, send_file
import machine, sys, neopixel, time

app = Microdot()

# Difine NeoPixel object
nbPixels = 12*2
pinPixelStrip = 16   # ESP32 D1 Mini
neoPixelStrip = neopixel.NeoPixel(machine.Pin(pinPixelStrip), nbPixels)

# Define status colors
statusColors = {
    'BUSY': (255,0,0),          # red
    'AVAILABLE': (0,255,0),     # green
    'AWAY': (246,190,0),        # cyan
    'OFF': (0, 0, 0),           # off
    'ON': (255, 255, 255)       # white
    }

# Store BusyLight default global status
blColor = statusColors.get('OFF')
blStatus = 'off'
blPreviousStatus='off'
blBrightness = 0.5 # Adjust the brightness (0.0 - 1.0)
    
def __setBrightness(color):
    r, g , b = color
    r = int(r * blBrightness)
    g = int(g * blBrightness)
    b = int(b * blBrightness)
    return (r, g, b)

def __setBusyLightColor(color, brightness):
    global blBrightness
    blBrightness = brightness
    global blColor
    blColor = color
    neoPixelStrip.fill(__setBrightness(color))
    neoPixelStrip.write()
    
    global blStatus
    blStatus = 'colored'

def __setBusyLightStatus(status):
    status = status.upper()
    color = statusColors.get(status)
    __setBusyLightColor(color, blBrightness)
    
    global blStatus
    blStatus = status.lower()

# Microdot APP routes

@app.get('/static/<path:path>')
async def staticRoutes(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return {'error': '4040 Not found'}, 404
    return send_file('static/' + path)

@app.get('/')
async def getIndex(request):
    return send_file('static/index.html')

@app.get('/api/brightness')
async def getBrightness(request):
    return {'brightness': blBrightness}

@app.post('/api/brightness')
async def setBrightness(request):
    brightness = request.json.get("brightness")
    
    if brightness is None:
        return {'error': 'missing brightness parameter'}, 400
    
    if type(brightness) is float \
       or type(brightness) is int:
        if brightness < 0 or brightness > 1:
            return {'error': 'brigthness out of bound (0.0 - 1.0)'}, 400
    else:
        return {'error': 'wrong brigthness type (float)'}, 400
    
    # Save blStatus
    global blStatus
    status = blStatus
    
    # Apply new brightness to current color
    color = blColor
    __setBusyLightColor(color, brightness)
    
    # Restore global status
    blStatus = status
    
    global blBrightness
    blBrightness = brightness
    
    return {'brightness': blBrightness}
    

@app.post('/api/color')
async def setColor(request):
    
    r = request.json.get("r")
    g = request.json.get("g")
    b = request.json.get("b")

    if bool(r is None or g is None or b is None):
        return {'error': 'missing color'}, 400
    else:
        if type(r) is int \
           and type(g) is int \
           and type(b) is int:
            color = (r, g, b)
        else:
            return {'error': 'wrong color type (int)'}, 400
        
    if (r < 0 or r > 255) \
       or (g < 0 or g > 255) \
       or (b < 0 or b > 255):
        return {'error': 'color out of bound (0 - 255)'}, 400
    
    brightness = request.json.get("brightness")
    
    if not brightness is None:
        if type(brightness) is float \
           or type(brightness) is int:
            if brightness < 0 or brightness > 1:
                return {'error': 'brightness out of bound (0.0 - 1.0)'}, 400
        else:
            return {'error': 'wrong brightness type (float)'}, 400
        __setBusyLightColor(color, brightness)
    
    __setBusyLightColor(color, blBrightness)

    return {'status': blStatus}

@app.route('/api/status/<status>', methods=['GET', 'POST'])
async def setStatus(request, status):
    lStatus = status.lower()
    if lStatus == 'on':
        __setBusyLightStatus('ON')
    elif lStatus == 'off':
        __setBusyLightStatus('OFF')
    elif lStatus == 'available':
        __setBusyLightStatus('AVAILABLE')
    elif lStatus == 'away':
        __setBusyLightStatus('AWAY')
    elif lStatus == 'busy':
        __setBusyLightStatus('BUSY')
    else:
        return {'error': 'unknown /api/status/' + lStatus + ' route'}, 404
    
    return {'status': blStatus}

@app.get('/api/color')
async def getColor(request):
    r, g, b = neoPixelStrip.__getitem__(0)
    return {'color': {'r': r, 'g': g, 'b': b}}

@app.get('/api/status')
async def getStatus(request):
    return {'status': blStatus}

@app.get('/api/debug')
async def getDebugInfo(request):
    r, g, b = blColor
    dr, dg, db = neoPixelStrip.__getitem__(0)
    return {'status': blStatus, 'brightness': blBrightness, 'color': {'r': r, 'g': g, 'b': b}, 'dimColor': {'r': dr, 'g': dg, 'b': db}}

@app.post('/api/mutedeck-webhook')
async def mutedeckWebhook(request):
    
    if request.json.get('control') != 'system':
        if request.json.get('call') == 'active':
            if request.json.get('mute') == 'active':
                isMuted = True
            else:
                isMuted = False
                
            if request.json.get('video') == 'active':
                isVideoOn = True
            else: 
                isVideoOn = False
                
            if isMuted: 
                __setBusyLightStatus('away')
            else:  
                __setBusyLightStatus('busy')
    else:
        __setBusyLightStatus('available')

    return {'status': blStatus}


@app.post('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

# Startup effect
def startUpSeq():
    print('Start seq begins')
    __setBusyLightStatus('OFF')
    time.sleep_ms(100)
    __setBusyLightStatus('BUSY')
    time.sleep_ms(125)
    __setBusyLightStatus('AWAY')
    time.sleep_ms(250)
    __setBusyLightStatus('AVAILABLE')
    time.sleep_ms(500)
    __setBusyLightStatus('OFF')
    print('Start seq is ended')
    
startUpSeq()
        
# Start API webserver
if __name__ == '__main__':
    app.run(port=80, debug=True)