const socketIO = require('socket.io');
const nodeStatic = require('node-static');
const fs = require('fs');
const https = require('https');

// SSL 인증서 설정
const options = {
    key: fs.readFileSync('private-key.pem'),
    cert: fs.readFileSync('public-cert.pem')
};

// HTTPS 서버 생성
let fileServer = new(nodeStatic.Server)();
let app = https.createServer(options, (req, res) => {
    fileServer.serve(req, res);
}).listen(8887);

// Socket.io 연결
let io = new socketIO.Server(app);
io.on('connection', socket => {
    // 방 생성 또는 참가
    socket.on('create or join', room => {
        let clients = io.sockets.adapter.rooms.get(room);
        let numClients = clients ? clients.size : 0;

        if (numClients === 0) {
            socket.join(room);
            socket.emit('created', room, socket.id);
        } else if (numClients === 1) {
            io.to(room).emit('join', room);
            socket.join(room);
            socket.emit('joined', room, socket.id);
            io.to(room).emit('ready');
        } else {
            socket.emit('full', room);
        }
    });

    // SDP/ICE 메시지 전달
    socket.on('offer', e => socket.broadcast.emit('offer', e));
    socket.on('answer', e => socket.broadcast.emit('answer', e));
    socket.on('candidate', e => socket.broadcast.emit('candidate', e));
});