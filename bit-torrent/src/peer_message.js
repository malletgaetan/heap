const { getId } = require('./utils.js')
// everything here is specification related, go README.md (wiki link is the best)

// build handshake buffer
const buildHandshake = torrent => {
    const buf = Buffer.alloc(68)
    buf.writeUInt8(19, 0)
    buf.write('BitTorrent protocol', 1)
    buf.writeUInt32BE(0, 20)
    buf.writeUInt32BE(0, 24)
    torrent.getInfoHash().copy(buf, 28)
    getId().copy(buf, 49)
    return buf
}

const buildUinterested = () => {
    const buf = Buffer.alloc(5)
    buf.writeUInt32BE(1, 0)
    buf.writeUInt8(3, 4)
    return buf
}

const buildInterested = () => {
    const buf = Buffer.alloc(5)
    buf.writeUInt32BE(1, 0)
    buf.writeUInt8(2, 4)
    return buf
}

const parse = msg => {
    const id = msg.length > 4 ? msg.readInt8(4) : null;
    let payload = msg.length > 5 ? msg.slice(5) : null;
    if (id === 6 || id === 7 || id === 8) {
        const rest = payload.slice(8);
        payload = {
        index: payload.readInt32BE(0),
        begin: payload.readInt32BE(4)
        };
        payload[id === 7 ? 'block' : 'length'] = rest;
    }

    return {
        size : msg.readInt32BE(0),
        id : id,
        payload : payload
    }
}

const buildRequest = (index, begin) => {
    const buf = Buffer.alloc(17)
    buf.writeUInt32BE(13, 0)
    buf.writeUInt8(6, 4)
    buf.writeUInt32BE(index, 5)
    buf.writeUInt32BE(begin, 9)
    buf.writeUInt32BE(Math.pow(2, 14), 13)
    return buf
}

module.exports = {
    buildHandshake,
    buildInterested,
    buildUinterested,
    parse,
    buildRequest,
}