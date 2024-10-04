async function setStatus(status = '') {
    // Les options par défaut sont indiquées par *
    const response = await fetch(`/api/status/${status}`, {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      headers: {
        "Content-Type": "application/json"
      }
    });
    return response.json(); // transforme la réponse JSON reçue en objet JavaScript natif
  }
  
async function getStatus() {
    // Les options par défaut sont indiquées par *
    const response = await fetch(`/api/status`, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      cache: "no-cache" // *default, no-cache, reload, force-cache, only-if-cached
    });
    return response.json(); // transforme la réponse JSON reçue en objet JavaScript natif
  }

async function setColor(color = {}) {
  // Les options par défaut sont indiquées par *
  const response = await fetch(`/api/color`, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(color) // le type utilisé pour le corps doit correspondre à l'en-tête "Content-Type"
  });
  return response.json(); // transforme la réponse JSON reçue en objet JavaScript natif
}

async function getColor() {
  // Les options par défaut sont indiquées par *
  const response = await fetch(`/api/color`, {
    method: "GET", // *GET, POST, PUT, DELETE, etc.
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    headers: {
      "Content-Type": "application/json"
    }
  });
  return response.json(); // transforme la réponse JSON reçue en objet JavaScript natif
}

async function setBrightness(brightness = {}) {
  // Les options par défaut sont indiquées par *
  const response = await fetch(`/api/brightness`, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(brightness) // le type utilisé pour le corps doit correspondre à l'en-tête "Content-Type"
  });
  return response.json(); // transforme la réponse JSON reçue en objet JavaScript natif
}

async function getBrightness() {
  // Les options par défaut sont indiquées par *
  const response = await fetch(`/api/brightness`, {
    method: "GET", // *GET, POST, PUT, DELETE, etc.
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    headers: {
      "Content-Type": "application/json"
    }
  });
  return response.json(); // transforme la réponse JSON reçue en objet JavaScript natif
}