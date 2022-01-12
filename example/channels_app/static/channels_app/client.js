const socket = new WebSocket("ws://localhost:8000/ws/test/");

socket.onmessage = function ({ data }) {
    const parsed_data = JSON.parse(data);
    console.log(parsed_data);
};

socket.onopen = () => {
    console.log("websocket connected...");
    socket.send(
        JSON.stringify({
            type: "message",
            data: {
                text: "hello",
            },
        })
    );
};
