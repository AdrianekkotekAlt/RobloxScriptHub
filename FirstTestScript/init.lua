local HttpService = game:GetService("HttpService")

local API = "https://robloxscripthub-kfz9.onrender.com/create-session"

local key = "YOUR_KEY"

local res = request({
    Url = API,
    Method = "POST",
    Headers = {["Content-Type"] = "application/json"},
    Body = HttpService:JSONEncode({
        key = key,
        userId = game.Players.LocalPlayer.UserId
    })
})

local data = HttpService:JSONDecode(res.Body)

if not data.valid then
    return print("Invalid key")
end

-- STORE SESSION TOKEN
getgenv().session_token = data.token

print("Session created")

-- load main script
loadstring(game:HttpGet("https://raw.githubusercontent.com/.../main.lua"))()
