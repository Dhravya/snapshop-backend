// Cloudflare worker to store files on IPFS
// So that we can use IPFS as a CDN
// This is a private CDN, so we need to authorize requests
// X-Api-Key will be used for that.

export default {
    async fetch(request, env) {
      const key = Date.now();
      const verbwire = require('verbwire')(env.get('VERBWIRE_API_KEY'));

  
      if (!authorizeRequest(request, env, key)) {
        return new Response("This is a private content delivery network.", {
          status: 403,
        });
      }

      switch (request.method) {
        case "PUT":
          fileUrl = await verbwire.store.file({
               filePath: request.body
          })['ipfs_storage']['ipfs_url']
          return new Response(fileUrl);
        default:
          return new Response("Method Not Allowed", {
            status: 405,
            headers: {
              Allow: "PUT",
            },
          });
      }
    },
  };
  // Check requests for a pre-shared secret
  const hasValidHeader = (request, env) => {
    return request.headers.get("X-Custom-Auth-Key") == "jaslkdfjjklajeuihadslfjsdlfjk";
  };
  function authorizeRequest(request, env, key) {
    switch (request.method) {
      case "PUT":
      case "DELETE":
        return hasValidHeader(request, env);
      case "GET":
        return key;
      default:
        return false;
    }
  }