function sendMessage() {
    let message = $("#peer_message").val()
    let peer = $("#peer_select").val()
    let token = "fix me"
    $.ajax({
        url: "send/" + peer + "/",
        data: {"msg": message},
        headers: {
            'X-CSRF-TOKEN': token
        },
        method: 'POST',
        success: function (data) {
            console.log('success: ' + data);
        }
    });
    //alert(thing.val()+" "+peer.val())
}

function doit(thing, t) {
    let eid = "in_" + thing

    let val = $("#" + eid)[0].value

    //token = $("input[name=csrfmiddlewaretoken]")[0].value
    let token = "fix the token"

    $.ajax({
        url: "save/" + thing + "/" + val + "/",
        data: {"type": t},
        headers: {
            'X-CSRF-TOKEN': token
        },
        method: 'POST',
        success: function (data) {
            console.log('succes: ' + data);
        }
    });
    //alert(thing+"="+val +" "+token)
}

console.log("we here now");
let s = new WebSocket("ws://192.168.1.110:3000","hive");
s.binaryType = 'arraybuffer';
console.log(s);
// s.send("hello")
s.onopen = function(event){
    //document.getElementById("headline").innerHTML = "CHAT - CONNECTED";
    console.log("<<< connected and open");
    s.send("hello\r\n");
};
s.onmessage = function(event) {
    console.log("RECEIVED: "+event.data);
    // var d=JSON.parse(event.data);
    // if (d.Type=="Chat") {
    //     $("#chat").append(wrapmessage(d));
    //     $("#chatdiv").animate({ scrollTop: $('#chatdiv').prop("scrollHeight")}, 1000);
    // } else if(d.Type=="userlist") {
    //     var ul = document.getElementById("userlist");
    //     while(ul.firstChild){ul.removeChild(ul.firstChild)};
    //     $("#userlist").append(wrapuser(d.Users));
    // } else if(d.Type=="Status"){
    //     document.getElementById("headline").innerHTML = "CHAT - connected - "+d.WSID;
    // }
};
console.log("<<< READY");


// import WebsocketClient from './modules/websocket-client.mjs'
// async function init_sock(){
//     const webSocketClient = new WebsocketClient;
//     await webSocketClient.connect('ws://192.168.1.110:3000/', 'hive');
//     webSocketClient.send('Hello!');
//     console.log(await webSocketClient.receive());
//
//     if (webSocketClient.dataAvailable !== 0) {
//         console.log(await webSocketClient.receive());
//     }
// }

// await init_sock();
