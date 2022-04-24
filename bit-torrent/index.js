const Torrent = require("./src/torrent.js")
const getPeers = require("./src/get_peers.js")
const download = require("./src/download.js")

async function main() {
    const torrent = new Torrent(process.argv[2])
    try {
        const peers = await getPeers(torrent)
        download(peers, torrent)
    } catch (err) {
        console.log(err)
    }
}

// everything starts here
main()
