const crypto = require("crypto")
const bencode = require("bencode")
const dgram = require("dgram")
const { getId } = require("./utils.js")


// build tracker handshake request 
const buildReqMessage = () => {
    const buf = Buffer.alloc(18)
    // protocol id 64bit integer
    buf.writeUInt32BE(0x417, 0)
    buf.writeUInt32BE(0x27101980, 4)
    // action
    buf.writeUInt32BE(0, 8)
    // transaction id
    crypto.randomBytes(4).copy(buf, 12)
    return buf
}

// check if message is a connect response or a announce response
const responseType = resp => {
    const action = resp.readUInt32BE(0)
    if (action === 0) return 'connect'
    if (action === 1) return 'announce'
}

const parseConnResp = resp => ({
    action: resp.readUInt32BE(0),
    transactionId: resp.readUInt32BE(4),
    connectionId: resp.slice(8),
})

// build tracker announce request
const buildAnnReq = (announce, torrent, port = 6881) => {
    const buf = Buffer.allocUnsafe(98)

    // connection id
    announce.connectionId.copy(buf, 0)
    // action
    buf.writeUInt32BE(1, 8)
    // transaction id
    crypto.randomBytes(4).copy(buf, 12)
    // info hash
    torrent.getInfoHash().copy(buf, 16)
    // peerId
    getId().copy(buf, 36)
    // downloaded
    Buffer.alloc(8).copy(buf, 56)
    // left
    torrent.getSize().copy(buf, 64)
    // uploaded
    Buffer.alloc(8).copy(buf, 72)
    // event
    buf.writeUInt32BE(0, 80)
    // ip address
    buf.writeUInt32BE(0, 84)
    // key
    crypto.randomBytes(4).copy(buf, 88)
    // num want
    buf.writeInt32BE(-1, 92)
    // port
    buf.writeUInt16BE(port, 96)

    return buf
}

const parseAnnResp = resp => {
    function group(iterable, groupSize) {
        let groups = []
        for (let i = 0; i < iterable.length; i += groupSize) {
            groups.push(iterable.slice(i, i + groupSize))
        }
        return groups
    }

    return {
        action: resp.readUInt32BE(0),
        transactionId: resp.readUInt32BE(4),
        leechers: resp.readUInt32BE(8),
        seeders: resp.readUInt32BE(12),
        peers: group(resp.slice(20), 6).map(address => {
            return {
                ip: address.slice(0, 4).join('.'),
                port: address.readUInt16BE(4)
            }
        })
    }
}

// getPeers request torrent tracker for peers informations and returns it as javascript object
module.exports = torrent => new Promise((res, rej) => {
    const url = torrent.getTrackerURL()
    if (!url) rej(new Error("Torrent not compatible, try with an other one!"))
    const udpsocket = dgram.createSocket("udp4")
    const reqmsg = buildReqMessage()
    // listen for incoming msg
    udpsocket.on("message", msg => {
        if (responseType(msg) === 'connect') {
            const connMsg = parseConnResp(msg)
            const announceMsg = buildAnnReq(connMsg, torrent)
            udpsocket.send(announceMsg, 0, announceMsg.length, url.port, url.hostname, err => {
                if(err) {
                    udpsocket.close()
                    rej(err)
                }
            })
        } else if (responseType(msg) === 'announce') {
            const announce = parseAnnResp(msg)
            udpsocket.close()
            res(announce)
        }
    })

    udpsocket.send(reqmsg, 0, reqmsg.length, url.port, url.hostname, err => {
        if(err){
            udpsocket.close()
            rej(err)
        } 
    })
})
