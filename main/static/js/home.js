const { CloseOutlined } = require("@mui/icons-material");

function logOut()
{
    var user_token = "{{ token }}";
    user_token = None;
}

document.getElementById("logout").addEventListener("click", function(logOut){
    logOut.preventDefault();
    logOut();
    console.log("LogOut Completed\n");
});