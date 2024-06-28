addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
  })
  
  async function handleRequest(request) {
    const url = new URL(request.url);
  
    if (url.pathname === "/salesAPI/v1") {
      const data = await ITEMS_DATA.get("item_data");
      if (data === null) {
        return new Response("Data not found", { status: 404 });
      }
  
      return new Response(data, {
        headers: { 
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS'
        },
      });
    }
  
    return new Response("Resource not found", { status: 404 });
  }