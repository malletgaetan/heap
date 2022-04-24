const { request } = require("http")
const net = require("net")
const message = require("./peer_message.js")

const HASH_LENGTH = 20
const piecesQueue = []
let done = false
let pieceLength = 0

// construction of the Queue of pieces (if piece in queue, then should be downloaded)
const initPiecesQueue = (pieces) => {
    let i = 0
    while(i <= pieces.length - HASH_LENGTH){
        piecesQueue.push({
            index: i,
            hash: pieces.slice(i, i+HASH_LENGTH),
            begin: 0,
            state: 0, // 0 not requested / 1 requested / 3 downloading / 4 complete
        })
        i += HASH_LENGTH
    }
}

// start a tcp connection with a peer and try to download data from it
const downloadFromPeer = (torrent, peer) => {
    let piece = piecesQueue.shift()
    const socket = new net.Socket()
    let buf = Buffer.alloc(0)
    let handshake = true
    socket.state = "choked"

    socket.on("error", (err) => {
        console.log(err)
        socket.end()
    })

    socket.connect(peer.port, peer.ip, () => {
        const handshake = message.buildHandshake(torrent)
        socket.write(handshake)
        // socket.end()
    })

    socket.on('data', recvBuf => {
        // +49 => in response to handhake, 'server' is supposed to respond same message handshake
        // +4 => reading how many bytes long will be the message, + the 4 actually used to transport this number
        const getMsgLen = () => handshake ? buf.readUInt8(0) + 49 : buf.readInt32BE(0) + 4
        buf = Buffer.concat([buf, recvBuf])

        // can we read the msg len && do message is complete
        if(buf.length >= 4 && buf.length >= getMsgLen()){
            msgHandler(buf.slice(0, getMsgLen()), socket, torrent)
            buf = buf.slice(getMsgLen(), buf.length)
            handshake = false
        }
        // when 'message' complete, call msgHandler
    })
}

const isCorrectHash = (msg, torrent) => {
    if (Buffer.compare(msg, torrent.getInfoHash()) == 0) return true
    return false
}


// WAIT THE UNCHOKE BEFORE REQUESTING!!!
// handshake done!
// Recevied a message with id =  5
// Recevied a message with id =  1

// identify message by its id and execute correct action from it
const msgHandler = (msg, socket) => {
    if (isHandshake(msg)) {
        // const isHashCorrect = isCorrectHash(msg, torrent)
        // if (!isHashCorrect) {
        //     socket.write(message.buildUinterested(), () => socket.close())
        //     return
        // }
        // console.log("handshake done!")
        socket.write(message.buildInterested())
    } else {
        const parsed = message.parse(msg)
        console.log("Recevied a message with id =", parsed.id)
        if (parsed.id === 1) unchokeHandler(socket)
        if (parsed.id === 5) socket.bitfield = parsed.payload
        if (parsed.id === 7) console.log("Received a piece!")
    }
}

const isHandshake = msg => {
  return msg.length === msg.readUInt8(0) + 49 && msg.toString('utf8', 1, 20) === 'BitTorrent protocol'
}

const chokeHandler = socket => {
    socket.state = "choked"
}

const unchokeHandler = socket => {
    socket.state = "unchoked"
    requestPiece(socket)
}

const requestPiece = socket => {
    if (socket.state === "choked") return
    for(let i = 0; i < piecesQueue.length; i++){
        if(!piecesQueue[i].isAfk) continue
        socket.pieceIndex = i
        piecesQueue[i] = false
        console.log("sent piece request")
        socket.write(message.buildRequest(i, begin))
        return
    }
}


// dowload function
module.exports = (peers, torrent) => {
    pieceLength = torrent.getPieceLength()
    initPiecesQueue(torrent.getPieces())
    downloadFromPeer(torrent, peers.peers[11])
}