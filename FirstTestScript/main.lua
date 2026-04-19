local HttpService = game:GetService("HttpService")

local API = "https://robloxscripthub-kfz9.onrender.com/validate-session"

local token = getgenv().session_token

if not token then
    return print("No session token")
end

local res = request({
    Url = API,
    Method = "POST",
    Headers = {["Content-Type"] = "application/json"},
    Body = HttpService:JSONEncode({
        token = token,
        userId = game.Players.LocalPlayer.UserId
    })
})

local data = HttpService:JSONDecode(res.Body)

if not data.valid then
    return print("Session invalid")
end

print("Main script fully unlocked")
