const fs = require("fs")
const bencode = require("bencode")
const crypto = require("crypto")
const urlParse = require("url").parse

module.exports = class {
    constructor(path) {
        this.path = path
        this.torrent = bencode.decode(fs.readFileSync(path))
    }

    // retrieve tracker URL from torrent file
    getTrackerURL() {
        if(!this.torrent.announce) return
        if(this.trackerURL) return this.trackerURL
        this.trackerURL = urlParse(this.torrent.announce.toString("utf8"))
        return this.trackerURL
    }

    // hash the info properties of the torrent to get a torrent identifier
    getInfoHash() {
        if(this.infoHash) return this.infoHash
        this.infoHash = crypto.createHash("sha1").update(bencode.encode(this.torrent["info"])).digest()
        return this.infoHash
    }

    // get total bytes size of file to download
    getSize() {
        if (this.size) return this.size
        this.size = Buffer.alloc(8)
        const size = BigInt(this.torrent.info.files ?
        this.torrent.info.files.map(file => file.length).reduce((a, b) => a + b) :
        this.torrent.info.length)
        this.size.writeBigInt64BE(size)
        return this.size 
    }

    // get buffer of concatenated SHA1 of every piece
    getPieces() {
        return this.torrent.info.pieces
    }

    // get bytes length of a piece
    getPieceLength() {
        return this.torrent.info["pieces length"]
    }

    // return javascript object of torrent file
    getTorrent() {
        return this.torrent
    }
}